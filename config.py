from dataclasses import dataclass
from pathlib import Path
import shutil

from fastapi import FastAPI


@dataclass
class TestSettings:
    root_dir = Path(__file__).parent.absolute()
    log_dir_test: Path = Path(root_dir).joinpath('logs/test')
    csv_dir_test: Path = log_dir_test.joinpath('csv')
    #nodes_dir_test: Path = Path(root_dir).joinpath('nodes')
    #test_validation_data_dir: Path = Path(root_dir).joinpath('NodeCore/test_nodes/csv_testdata')

test_settings=TestSettings()


@dataclass
class Logs:
    txt_dir: Path = Path('xxxx')
    csv_dir: Path = Path('xxxx')

@dataclass
class WwwServer:
    port: int = 8079

@dataclass
class FileSystem:
    root: Path = Path(__file__).parent
    node_dir: Path = root.joinpath('app/nodes')
    node_module_loc: Path = 'app.nodes'

@dataclass
class Settings:
    www: WwwServer = WwwServer()
    logs: Logs = Logs()
    filesystem: FileSystem = FileSystem()

settings=Settings()
app_fastapi = FastAPI(title='MavicMax', version='1.0')

if __name__ == "__main__":
    print(settings.logs.txt_dir)
    print(settings.filesystem.root)


