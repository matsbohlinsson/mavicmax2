import _thread
import logging
import time
import traceback
from pathlib import Path
from typing import Optional

from fastapi import Request

import uvicorn
from fastapi import FastAPI

import NodeCore
import app.gui
import DroneSdk
import config

Sdk=DroneSdk.get_drone_sdk()
import MavicMaxGui
from app.startup.autostart import start_autostart

try:
    import MavicMaxGui.RUNTEST_GUI
except:
    traceback.print_stack()
log = logging.getLogger(__name__)


#from sse_starlette.sse import EventSourceResponse
fastapi_app = FastAPI(title='MavicMax', version='1.0')
def startup_fastapi():
    uvicorn.run("app.startup.main:fastapi_app",host='0.0.0.0', port=4557)
    #uvicorn.run("main:fastapi_app",host='0.0.0.0', port=4557, reload=True, debug=True, workers=3)
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



def startup_remi(android_activity):
    try:
        print(f"startup_test_dji_remove_me:{android_activity}")
        app.gui.run(port=8079)
        time.sleep(0.1)

        DroneSdk.get_drone_sdk().Ui.update_url_touch("http://127.0.0.1:8079")
        log.info(f"CSV logdir:{NodeCore.LOGDIR.as_posix()}")
        log.info("First")
    except:
        print(traceback.format_exc())




def startup(android_activity):
    import DroneSdk.AndroidBindings
    DroneSdk.AndroidBindings.DjiBindings.init(android_activity)
    logfile = DroneSdk.get_drone_sdk().Admin.get_log_dir() + '/mavicmax2.log'
    logging.basicConfig(filename=logfile, level=logging.INFO,
                        format='%(asctime)s,%(msecs)d %(levelname)-8s  %(message)s [%(funcName)s() %(filename)s:%(lineno)d]',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        force=True)
    NodeCore.LOGDIR = Path(DroneSdk.get_drone_sdk().Admin.get_log_dir() + '/csv')
    try:
        _thread.start_new_thread(startup_remi, (android_activity,))
        start_autostart()
        startup_fastapi()
    except:
        print(traceback.format_exc())


class Activity:
    def getFilesDir(self):
        return '/fake/a'

if __name__ == "__main__":
    startup(Activity())
    time.sleep(100)



def testme():
    api = DroneSdk.AndroidBindings.DjiBindings
    #api.show_toast("Start")
    api.beep()
    time.sleep(1)
    api.beep(freq=2)
    time.sleep(1)
    api.start_simulator(58,11)
    time.sleep(2)
    api.takeoff()
    time.sleep(10)
    api.beep(freq=2)
    #api.start_virtual_sticks()
    #Flightctrl.set_speed(course=100, speed=10.5, height=10.5, heading=91, duration=30)
    #Flightctrl
    #api.send_virtual_stick_raw()

'''
def git_puller() -> str:
    api = DroneSdk.AndroidDjiBindings.DjiBindings
        s = MavicMaxLib.util.git.pull()
        if "Already-up-to-date" not in s:
            api.ui.beep()
            MavicGlobals.popup("git pull",s)
            if auto_restart:
                api.ui.restart_app()
    return "OK:"+str(api.private.fast_loop()) + " " + str(api.drone.rth_is_going_home())
'''



def startup_test_dji_remove_me(android_activity):
    print(f"EEEEE:{android_activity}")
    MavicMaxGui.RUNTEST_GUI.run()
    android_activity.pythonToAndroid.doNothing()
    time.sleep(5)
    android_activity.pythonToAndroid.startSimulator(59,12)
    print(f"EEEEE:Simulator started")
    time.sleep(5)
    android_activity.pythonToAndroid.takeoff()
    time.sleep(60)
    #android_activity.pythonToAndroid.restartApp()

