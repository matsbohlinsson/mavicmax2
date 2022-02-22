from pathlib import Path
import NodeCore
import config


def run():
    test_nodes_path = Path(__file__).parent
    nodes_path = test_nodes_path.joinpath('nodes')
    csv_dir_path = test_nodes_path.joinpath('nodes/csv_testdata')
    exclude=['app.nodes.test_nodes.test_in_out1',
             'app.nodes.test_nodes.test_in_out2',
             'app.nodes.test_nodes.test_in_out3',
             'app.nodes.drone.telemetry',
             'app.nodes.admin.git',
             'app.nodes.admin.log',
             'app.nodes.drone.remotecontroller']
    return NodeCore.run_self_test(modules_dir=nodes_path, csv_dir_path=csv_dir_path, repeat=2, exclude=exclude)
if __name__ == "__main__":
    NodeCore.LOGDIR = config.test_settings.log_dir_test.joinpath('app')
    exit(run())


