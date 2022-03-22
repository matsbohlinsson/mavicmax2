import traceback

from NodeCore import runner2
from app import util


def start_autostart():
    try:
        pass
        if util.platform.is_running_on_android():
            runner2.NodeRunner.start_node('/admin/git',{'autopull': True})
            runner2.NodeRunner.start_node('/admin/log',{})
    except:
        print(traceback.format_exc())

    pass

