import logging

import DroneSdk.bindings.AndroidBindings as android
import DroneSdk.bindings.PcSimulatorBindings as desktop
from DroneSdk import models
from fastapi import FastAPI
from app.util import platform, grep_log

log = logging.getLogger(__file__)

current_sdk= android.DjiBindings if platform.is_running_on_android() else desktop.SimBindings
app_fastapi = FastAPI(title='MavicMax', version='1.0')

#########
# Drone #
#########
@app_fastapi.post("/start_simulator")
def start_simulator(lat:float = 58.12345, lon: float=11.987654):
    current_sdk.start_simulator(lat, lon)
    return "OK"

@app_fastapi.post("/get_drone_telemetry", response_model=models.Telemetry)
def get_drone_telemetry() -> models.Telemetry:
    return current_sdk.get_drone_telemetry()

@app_fastapi.post("/takeoff")
def get_drone_takeoff() -> str:
    current_sdk.takeoff()
    return "OK"

@app_fastapi.post("/set_speed")
def set_speed(course: float = 45, speed: float = 0.5, height: float = 5.5, heading: float = 23, duration: float = 1.5):
    current_sdk.set_speed(course, speed, height, heading, duration)

@app_fastapi.post("/start_motors")
def start_motors():
    current_sdk.start_motors()

@app_fastapi.post("/get_rc_telemetry", response_model=models.Rc)
def get_rc_telemetry() -> models.Rc:
    return current_sdk.get_rc_inputs()

#########
#  APP  #
#########
from fastapi.responses import PlainTextResponse
@app_fastapi.get("/get_log", response_class=PlainTextResponse)
async def get_log(filename: str='mavicmax2.log', last_lines=250, grep='', exclude='_message(', ):
    logfile_abs = current_sdk.get_log_dir() + f'/{filename}'
    return grep_log(logfile_abs, grep, exclude, int(last_lines))

@app_fastapi.post("/update_url_touch")
def update_url_touch(url:str):
    current_sdk.update_url_touch(url)
    return "OK"

@app_fastapi.post("/get_log_dir")
def get_log_dir():
    return current_sdk.get_log_dir()

@app_fastapi.post("/test")
def fastapi_test():
    return "test_ok"

@app_fastapi.get("/restart")
async def restart():
    current_sdk.restart_app()
    return "Restarting"

@app_fastapi.get("/get_app_root")
def get_app_root() -> str:
    return current_sdk.get_app_root()


#########
#  GIT  #
#########
@app_fastapi.get("/get_git_branch")
def get_git_branch() -> str:
    return current_sdk.get_app_root()


if __name__=="__main__":
    import uvicorn
    uvicorn.run("sdk:app_fastapi",host='0.0.0.0', port=4558, reload=True, debug=True, workers=3)
