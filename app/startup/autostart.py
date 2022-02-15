import traceback

from NodeCore import runner2


def start_autostart():
    try:
        pass
        runner2.NodeRunner.start_node('/admin/git',{'autopull': True})
        runner2.NodeRunner.start_node('/admin/log',{})
    except:
        print(traceback.format_exc())

    pass

