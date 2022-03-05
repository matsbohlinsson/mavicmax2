import dataclasses
import logging
import math
import time
from typing import Optional
from urllib.request import Request

import uvicorn
from sse_starlette import EventSourceResponse

import DroneSdk.bindings.AndroidBindings
import DroneSdk.bindings.PcSimulatorBindings
from DroneSdk import models
from fastapi import FastAPI

from app.util import platform

log = logging.getLogger(__file__)
current_sdk=DroneSdk.bindings.AndroidBindings
'''
if platform.is_running_on_android():
    current_sdk = DroneSdk.bindings.AndroidBindings.DjiBindings
else:
    current_sdk = DroneSdk.bindings.PcSimulatorBindings
'''

#bindings=DroneSdk.bindings.PcSimulatorBindings
app = FastAPI(title='MavicMax', version='1.0')


@app.post("get_drone_telemetry", response_model=models.Telemetry)
def get_drone_telemetry() -> models.Telemetry:
    return current_sdk.DjiBindings.get_telemetry()

@app.post("get_rc_telemetry", response_model=models.Rc)
def get_rc_telemetry() -> models.Rc:
    return current_sdk.DjiBindings.get_rc_inputs()


#@app.post("start_simulator/{lat}/{lon}")
@app.post("start_simulator")
def start_simulator(self, lat:float = 58.1111, lon: float=11.010203):
    current_sdk.DjiBindings.start_simulator(lat, lon)

@app.post("update_url_touch")
def update_url_touch(url:str):
    current_sdk.DjiBindings.update_url_touch(url)

@app.post("get_log_dir")
def get_log_dir():
    return current_sdk.DjiBindings.get_log_dir()


#import DroneSdk.sd

    #uvicorn.run("app.startup.main:fastapi_app",host='0.0.0.0', port=4557)
    #uvicorn.run("main:fastapi_app",host='0.0.0.0', port=4557, reload=True, debug=True, workers=3)

'''
#from sse_starlette.sse import EventSourceResponse
@fastapi_app.get("/")
def read_root():
    return {"Hello": "World"}

def logGenerator(request, prestring):
    for i in range(0,100):
        yield f'{prestring} now{i}'
        time.sleep(0.1)
@fastapi_app.get('/stream-logs')
async def run(request: Request, prestring):
    event_generator = logGenerator(request, prestring)
    return EventSourceResponse(event_generator)
@fastapi_app.get("/items/{item_id}")
def read_item(item_id: int, q: Optional[str] = None):
    """
    Create an item with all the information:

    - **name**: each item must have a name
    - **description**: a long description
    - **price**: required
    - **tax**: if the item doesn't have tax, you can omit this
    - **tags**: a set of unique tag strings for this item
    \f
    :param item: User input.
    """
    return {"item_id": item_id, "q": q}
'''

if __name__=="__main__":
    uvicorn.run("sdk:app",host='0.0.0.0', port=4558, reload=True, debug=True, workers=3)
