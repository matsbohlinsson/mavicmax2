import app.RUNTEST_APP
import MavicMaxGui.RUNTEST_GUI
import NodeCore.test_nodes.RUNTEST_NODE
import config

NodeCore.LOGDIR = config.test_settings.log_dir_test

def run():
    run_list=[
        app.RUNTEST_APP,
        NodeCore.test_nodes.RUNTEST_NODE,
        MavicMaxGui.RUNTEST_GUI
    ]
    for module in run_list:
        print(f'Running:{module.__name__}')
        func = module.run
        exitcode = func()
        if exitcode!=0: exit(1)



if __name__ == "__main__":
    run()

