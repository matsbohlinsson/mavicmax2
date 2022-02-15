import dataclasses
import logging
import math

import DroneSdk.AndroidBindings
from simulated_app_root_logs_userdata import get_simulated_app_root

log = logging.getLogger(__file__)

class Sdk:
    class _Admin:
        def __init__(self):
            pass
        def restart_app(self):
            pass
        def get_log_dir(self):
            return Sdk.FileSystem.get_app_root()+'/logs/20220101_0101'

    Admin=_Admin()

    class _Ui:
        def __init__(self):
            self.api = DroneSdk.AndroidBindings.DjiBindings
        def update_url_touch(self, url:str):
            log.info(f"update_url_touch({url})")
    Ui=_Ui()

    class _Rc:
        rc_lx: float = 0.0
        rc_ly: float = 0.0
        rc_rx: float = 0.0
        rc_ry: float = 0.0
        rc_lat: float = 0.0
        rc_lon: float = 0.0
        rc_alt: float = 0.0
        rc_speed: float = 0.0
        rc_baro_alt: float = 0.0
        rc_time: float = 0.0
        rc_acc: float = 0.0

        def __init__(self):
            self.api = DroneSdk.AndroidBindings.DjiBindings

        def update(self):
            try:
                self.rc_lat = 0.0
                self.rc_lon = 0.0
                self.rc_alt = 0.0
                self.rc_speed = 0.0
                self.rc_baro_alt = 0.0
                self.rc_time = 0.0
                self.rc_acc = 0.0
                self.rc_lx = 0.0
                self.rc_ly = 0.0
                self.rc_rx = 0.0
                self.rc_ry = 0.0

            except:
                log.exception("telemetry")
    Rc=_Rc()


    class _Flightcontroller:

        def __init__(self):
            pass

        def start_motors(self):
            pass

        def take_off(self):
            pass

        def set_speed(self, course: float = None, speed: float = 0, height: float = None, heading: float = None, duration:float=1.5):
            pass

        def start_simulator(self, lat: float=58.11111,lon: float = 11.1111111):
            pass
    Flightctrl=_Flightcontroller()

    @dataclasses.dataclass
    class _Telemetry:
        speed_x: float = 0.0
        speed_y: float = 0.0
        speed_z: float = 0.0
        speed_xy: float = 0.0
        course: float = 0.0
        yaw: float = 0.0
        pitch: float = 0.0
        roll: float = 0.0
        lat: float = 12.11111111
        lon: float = 13.11111111
        height: float = 0.0
        is_flying: int = 0.0
        gps_level: int = -1
        flight_mode: str = 'xxxxxxxxx'
        drone_type: str = 'xxxxxxxxx'
        terrain_height: float = -1.0
        motor_on_nbr: int = -1
        rpm: int = -1
        flytime: int = -1
        state: str = 'xxxxxxxxx'

        '''
        public int getXSpeed() {
            return 0;
        }

        public int getYSpeed() {
            return 0;
        }

        public int getZSpeed() {
            return 0;
        }
        '''


        def __init__(self):
            pass

        def update(self):
            try:
                pass
            except:
                pass

        def calc_course(self, x:float,y:float):
            r = math.sqrt(x**2 + y**2)
            theta = math.atan2(y, x)
            degrees = math.degrees(theta)
            if degrees < 0:
                degrees += 360
            return degrees

    Telemetry=_Telemetry()

    class _Git:
        def __init__(self, dir:str, url:str):
            pass

        def clone(self, dir, url):
            pass

        def diff(self):
            pass

        def commit_all(self, message='From app'):
            pass

        def status(self):
            pass

        def log(self):
            return f"Not impl in sim {__file__}"

        def get_branches(self) -> [str]:
            return [f"Not impl in sim {__file__}"]
            pass

        def pull(self, dir, branchName):
            return f"Not impl in sim {__file__}"

        def get_current_branch(self, dir):
            return f"Not impl in sim {__file__}"

        def checkout(self, branchName):
            log.info(f'Change branch to:{branchName}')
            return f"Not impl in sim {__file__}"

        def rm_dir(self):
            import shutil
            #shutil.rmtree(self.dir)



    Git=_Git('','') #_Git(self.python_root, self.python_root)

    class _FileSystem:
        def __init__(self):
            pass

        def get_app_root(self) -> str:
            return get_simulated_app_root()
    FileSystem=_FileSystem()
Sdk=Sdk()
