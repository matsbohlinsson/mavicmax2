from pathlib import Path
import NodeCore
import config


def run():
    test_nodes_path = Path(__file__).parent
    nodes_path = test_nodes_path.joinpath('nodes')
    csv_dir_path = test_nodes_path.joinpath('nodes/csv_testdata')
    return NodeCore.run_self_test(modules_dir=nodes_path, csv_dir_path=csv_dir_path, repeat=2)
if __name__ == "__main__":
    NodeCore.LOGDIR = config.test_settings.log_dir_test.joinpath('app')
    exit(run())


