import logging

import DroneSdk.bindings.AndroidBindings as android
import DroneSdk.bindings.PcSimulatorBindings as desktop
from DroneSdk import models
from fastapi import FastAPI
from app.util import platform, grep_log

log = logging.getLogger(__file__)

current_sdk= android.DjiBindings if platform.is_running_on_android() else desktop.SimBindings
app_fastapi = FastAPI(title='MavicMax', version='1.0')

@app_fastapi.post("/get_drone_telemetry", response_model=models.Telemetry)
def get_drone_telemetry() -> models.Telemetry:
    return current_sdk.get_telemetry()

@app_fastapi.post("/get_rc_telemetry", response_model=models.Rc)
def get_rc_telemetry() -> models.Rc:
    return current_sdk.get_rc_inputs()

@app_fastapi.post("/start_simulator")
def start_simulator(self, lat:float = 58.1111, lon: float=11.010203):
    current_sdk.start_simulator(lat, lon)

@app_fastapi.post("/update_url_touch")
def update_url_touch(url:str):
    current_sdk.update_url_touch(url)

@app_fastapi.post("/get_log_dir")
def get_log_dir():
    return current_sdk.get_log_dir()

@app_fastapi.post("/test")
def fastapi_test():
    return "test_ok"

from fastapi.responses import PlainTextResponse
@app_fastapi.get("/get_log", response_class=PlainTextResponse)
async def get_log(filename: str='mavicmax2.log', last_lines=250, grep='', exclude='_message(', ):
    logfile_abs = current_sdk.get_log_dir() + f'/{filename}'
    return grep_log(logfile_abs, grep, exclude, int(last_lines))

@app_fastapi.get("/restart")
async def restart():
    current_sdk.restart_app()
    return "Restarting"

@app_fastapi.get("/get_app_root")
def get_app_root(self) -> str:
    return current_sdk.get_app_root()

@app_fastapi.get("/get_app_root")
def get_git_branch(self) -> str:
    return current_sdk.get_app_root()


if __name__=="__main__":
    import uvicorn
    uvicorn.run("sdk:app_fastapi",host='0.0.0.0', port=4558, reload=True, debug=True, workers=3)
