import logging

import DroneSdk.bindings.AndroidBindings
import DroneSdk.bindings.PcSimulatorBindings
from DroneSdk import models
from fastapi import FastAPI
from app.util import platform
log = logging.getLogger(__file__)

current_sdk=DroneSdk.bindings.AndroidBindings.DjiBindings
if platform.is_running_on_android():
    current_sdk = DroneSdk.bindings.AndroidBindings.DjiBindings
else:
    current_sdk = DroneSdk.bindings.PcSimulatorBindings.SimBindings

app_fastapi = FastAPI(title='MavicMax', version='1.0')


@app_fastapi.post("/get_drone_telemetry", response_model=models.Telemetry)
def get_drone_telemetry() -> models.Telemetry:
    return current_sdk.get_telemetry()

@app_fastapi.post("/get_rc_telemetry", response_model=models.Rc)
def get_rc_telemetry() -> models.Rc:
    return current_sdk.get_rc_inputs()


#@app.post("start_simulator/{lat}/{lon}")
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

if __name__=="__main__":
    import uvicorn
    uvicorn.run("sdk:app_fastapi",host='0.0.0.0', port=4558, reload=True, debug=True, workers=3)
