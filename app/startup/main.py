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
import MavicMaxGui
from app.startup.autostart import start_autostart

try:
    import MavicMaxGui.RUNTEST_GUI
except:
    traceback.print_stack()
log = logging.getLogger(__name__)
import DroneSdk.sdk as sdk


def startup_remi(android_activity):
    try:
        print(f"startup_test_dji_remove_me:{android_activity}")
        app.gui.run(port=8079)
        time.sleep(0.1)
        sdk.update_url_touch("http://127.0.0.1:8079")
        log.info(f"CSV logdir:{NodeCore.LOGDIR.as_posix()}")
    except:
        log.exception('startup_remi')


def startup(android_activity):
    import DroneSdk.bindings.AndroidBindings
    DroneSdk.bindings.AndroidBindings.DjiBindings.init(android_activity)
    logdir = DroneSdk.sdk.get_log_dir()
    logfile = logdir + '/mavicmax2.log'
    logging.basicConfig(filename=logfile, level=logging.INFO,
                        format='%(asctime)s,%(msecs)d %(levelname)-8s  %(message)s [%(funcName)s() %(filename)s:%(lineno)d]',
                        datefmt='%Y-%m-%d:%H:%M:%S',
                        force=True)
    NodeCore.LOGDIR = Path(logdir + '/csv')
    try:
        _thread.start_new_thread(startup_remi, (android_activity,))
        _thread.start_new_thread(start_autostart, ())
        import DroneSdk.sdk
        uvicorn.run("DroneSdk.sdk:app_fastapi", host='0.0.0.0', port=4557)
    except:
        print(traceback.format_exc())


if __name__ == "__main__":
    startup(None)
    time.sleep(100)
