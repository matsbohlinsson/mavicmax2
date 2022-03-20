import logging
import time
from enum import Enum
from pathlib import Path

import cv2
import numpy as np
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from starlette.responses import StreamingResponse, Response
import DroneSdk.bindings.AndroidBindings as android
import DroneSdk.bindings.PcSimulatorBindings as desktop
import config
from DroneSdk import models
from fastapi import FastAPI

from app import util
from app.util import platform, grep_log
from config import settings

log = logging.getLogger(__file__)

current_sdk= android.DjiBindings if platform.is_running_on_android() else desktop.SimBindings
app_fastapi = config.app_fastapi
#########
# Drone #
#########
@app_fastapi.post("/start_simulator", summary="Start drone built-in simulator")
def start_simulator(lat:float = 58.12345, lon: float=11.987654):
    """
    Start drone built in simulator with homepoint lat/lon
    - **lat**: Homepoint latitude
    - **lon**: Homepoint longitude
    """
    current_sdk.start_simulator(lat, lon)
    return "OK"

@app_fastapi.post("/get_drone_telemetry", response_model=models.Telemetry, summary="Returns drone data (speed height lat/lon and more)")
def get_drone_telemetry() -> models.Telemetry:
    return current_sdk.get_drone_telemetry()

@app_fastapi.post("/takeoff", summary="Start takeoff. Hovers 1.2m above ground")
def takeoff() -> str:
    current_sdk.takeoff()
    return "OK"

@app_fastapi.post("/set_speed", summary="Move drone with speed to direction and height")
def set_speed(direction: float = 45, speed: float = 0.5, height: float = 5.5, heading: float = 23, duration: float = 1.5):
    """
    Move drone with speed to direction and height
    - **direction**: Direction in 0-360 compass degrees 0.1 step
    - **speed**: Speed in m/s (0.1 step)
    - **height**: Goto height (in meters in (0.1m step)
    - **heading**: Set drone yaw (where camera usually points to)
    - **duration**: Keep speed for duration seconds
    """
    current_sdk.set_speed(direction, speed, height, heading, duration)

@app_fastapi.post("/start_motors",  summary="Start motors with idle speed.")
def start_motors():
    current_sdk.start_motors()
    return "OK"

@app_fastapi.post("/get_rc_telemetry", response_model=models.Rc,  summary="Returns remotecontroll data (stick, buttons, gps and more)")
def get_rc_telemetry() -> models.Rc:
    return current_sdk.get_rc_inputs()

@app_fastapi.post("/start_virtualstick", summary="Start virtualstick mode")
def start_virtual_sticks() -> str:
    current_sdk.start_virtual_sticks()
    return "OK"


#########
#  APP  #
#########
from fastapi.responses import PlainTextResponse
class LogType(str, Enum):
    app = "mavicmax2.log"
    logcat = "logcat.txt"

@app_fastapi.get("/get_log", response_class=PlainTextResponse, summary="Get current log from mobile device mavicmax2.log or logcat.txt")
async def get_log(logname:LogType, last_lines=250, grep='', exclude='_message(', ):
    logfile_abs = current_sdk.get_log_dir() + f'/{logname}'
    return grep_log(logfile_abs, grep, exclude, int(last_lines))

@app_fastapi.get("/restart", summary="Restart app on mobile device")
def restart():
    log.info("Restart")
    print("Restart")
    current_sdk.restart_app()
    return "Restarting"

@app_fastapi.post("/get_log_dir")
def get_log_dir():
    return current_sdk.get_log_dir()

@app_fastapi.get("/debug1")
def debug1():
    '''    for i in range(0, 100):
            # TODO Read out size from bitmap and use in newshape
            bitmap = api.ui.get_frame_bitmap_byte_array()
            deserialized_bytes = np.frombuffer(bitmap, dtype=np.uint8)
            conv = np.reshape(deserialized_bytes, newshape=(1080, 1920, 4))
            conv2 = cv2.cvtColor(conv, cv2.COLOR_BGRA2RGBA)
            image_data = cv2.resize(conv, (int(1080 / 2), int(1920 / 2)))
            conv3 = increase_brightness(conv2, 50)
            cv2.imwrite(filename, conv3)
    '''
    return "debug1_"

@app_fastapi.post("/update_url_touch")
def update_url_touch(url:str):
    current_sdk.update_url_touch(url)
    return "OK"

def getBitmapByteArray() -> bytearray:
    return current_sdk.getBitmapByteArray()

@app_fastapi.get('/save-frame-to-file')
def save_frame_to_file(filename: str, jpeg_compression: int=10):
    filepath = f'{get_app_root()}/{filename}'
    current_sdk.saveFrameToFile(filename=filepath, jpeg_compression=jpeg_compression)
    return filepath

@app_fastapi.get('/get_jpg_file')
def get_jpg_file(filename: str):
    filepath = f'{get_app_root()}/{filename}'
    b = Path(filepath).read_bytes()
    return Response(content=b, media_type="image/jpg")

@app_fastapi.get('/get_fpv_frame')
def get_fpv_frame(quality:int=20):
    fpv_file_name='current_fpv.jpg'
    save_frame_to_file(fpv_file_name, quality)
    return get_jpg_file(fpv_file_name)


@app_fastapi.get('/stream-fpv')
async def stream_fpv(request: Request, jpeg_compression=10, delay: float=0.1):
    def generate():
        while True:
            filename = 'stream.jpg'
            save_frame_to_file(filename=filename, jpeg_compression=int(jpeg_compression))
            time.sleep(float(delay))
            filepath = f'{get_app_root()}/{filename}'
            b = Path(filepath).read_bytes()
            yield (b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' +
                   bytearray(b) + b'\r\n')
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")



@app_fastapi.get('/stream-fpv-test')
async def stream_fpv_test(request: Request):
    def generate():
        cap = cv2.VideoCapture(0)
        while True:
            cap.grab()
            ret, frame = cap.read()
            # frame = cv2.resize(frame, None, fx=4, fy=4, interpolation=cv2.INTER_LINEAR)
            (flag, encodedImage) = cv2.imencode(".jpg", frame)
            yield (b'--frame\r\n' b'Content-Type: image/jpeg\r\n\r\n' +
                   bytearray(encodedImage) + b'\r\n')
    return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")



async def logGenerator(request):
    for line in [f'hej {x}' for x in range(100)]:
        if await request.is_disconnected():
            print("client disconnected!!!")
            break
        yield line
        time.sleep(0.5)

@app_fastapi.get('/stream-logs')
async def stream_logs(request: Request):
    event_generator = logGenerator(request)
    return EventSourceResponse(event_generator)



@app_fastapi.get("/get_app_root")
def get_app_root() -> str:
    return current_sdk.get_app_root()

@app_fastapi.get("/get_git_root")
def get_git_root() -> str:
    if util.platform.is_running_on_android():
        return current_sdk.get_app_root()+'/git/mavicmax2'
    return current_sdk.get_app_root()



'''
@app_fastapi.post("/test")
def fastapi_test():
    return "test_ok"



'''


#########
#  GIT  #
#########
@app_fastapi.get("/get_git_branch")
def get_git_branch(dir: str) -> str:
    return current_sdk.get_app_root()

@app_fastapi.get("/git_pull")
def git_pull(self, dir):
    return current_sdk.git_pull(dir)

@app_fastapi.get("/git_status")
def git_status(dir):
    return current_sdk.git_status(dir)


if __name__=="__main__":
    import uvicorn
    uvicorn.run("sdk:app_fastapi",host='0.0.0.0', port=4558, reload=True, debug=True, workers=3)
