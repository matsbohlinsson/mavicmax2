import dataclasses
import logging
import math
import DroneSdk.bindings.AndroidBindings
import DroneSdk.bindings.PcSimulatorBindings
from DroneSdk.dji import DjiKeys
log = logging.getLogger(__file__)

bindings=DroneSdk.bindings.PcSimulatorBindings.SimBindings
#bindings=DroneSdk.AndroidBindings.DjiBindings

class _Sdk:
    class _Helpers:
        VS_ADVANCED = 0
        VS_BODY = 1
        VS_YAW_SPEED = 3
        VS_VERT_ALT = 4
        VS_PITCH_SPEED = 6

        def getVirtualstickRawFlag(self, advanced, body, yawSpeed, vertAltitude, pitchSpeed):
            b=0
            if (advanced!=0): b+= (1<<Sdk._Helpers.VS_ADVANCED)
            if (body!=0): b+= (1<<Sdk._Helpers.VS_BODY)
            if (yawSpeed!=0): b+= (1<<Sdk._Helpers.VS_YAW_SPEED)
            if (vertAltitude!=0): b+= (1<<Sdk._Helpers.VS_VERT_ALT)
            if (pitchSpeed!=0): b+= (1<<Sdk._Helpers.VS_PITCH_SPEED)
            return b
    Helpers = _Helpers()


    class _Admin:
        def restart_app(self):
            bindings.restart_app()

        def get_log_dir(self):
            return bindings.get_log_dir()

    Admin=_Admin()

    class _Ui:
        def update_url_touch(self, url:str):
            bindings.update_url_touch(url)
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


        def update(self):
            def rawstick_to_float(value) -> float:
                value = float(value)
                return round((value - 1024) / 660, 4)

            try:
                rc_gps = bindings.get_rc_gps()
                self.rc_lat = rc_gps[0]
                self.rc_lon = rc_gps[1]
                self.rc_alt = rc_gps[2]
                self.rc_speed = rc_gps[3]
                self.rc_baro_alt = rc_gps[4]
                self.rc_time = rc_gps[5]
                self.rc_acc = rc_gps[6]
                rc_sticks = bindings.get_rc_inputs()
                self.rc_lx = rawstick_to_float(rc_sticks[0])
                self.rc_ly = rawstick_to_float(rc_sticks[1])
                self.rc_rx = rawstick_to_float(rc_sticks[2])
                self.rc_ry = rawstick_to_float(rc_sticks[3])

            except:
                log.exception("telemetry")
    Rc=_Rc()

    class _Flightcontroller:

        def start_motors(self):
            bindings.start_motors()

        def take_off(self):
            bindings.take_off()

        def set_speed(self, course: float = None, speed: float = 0, height: float = None, heading: float = None, duration:float=1.5):
            flag = Sdk.Helpers.getVirtualstickRawFlag(advanced=1, body=0, yawSpeed=0, vertAltitude=1, pitchSpeed=1)
            radBearing = math.radians(course)
            pitch = speed * math.cos(radBearing)
            roll = speed * math.sin(radBearing)
            yaw = heading
            bindings.send_virtual_stick_raw(flag=flag, throttle=height, roll=roll, pitch=pitch, yaw=yaw, duration=duration)

        def start_simulator(self, lat: float=58.11111,lon: float = 11.1111111):
            bindings.start_simulator(lat, lon)
    Flightctrl=_Flightcontroller()




    class _Keys:
        Key=DjiKeys.Keys

        def get(self, key:Key):
            return bindings.get_key_value(key.value)
        def set(self, key:Key, value):
            return bindings.set_key_value(key.value, value)
    Keys=_Keys()

    class _Git:
        def __init__(self, dir:str, url:str):
            self.dir=dir
            self.url=url

        def clone(self, dir, url):
            bindings.drone.drone.clone(dir, url, "", "")

        def diff(self):
            bindings.drone.drone.diff(self.dir)

        def commit_all(self, message='From app'):
            bindings.drone.drone.commit_all(self.dir, message)

        def status(self):
            return bindings.drone.drone.status(self.dir)

        def log(self):
            return "Not impl"

        def get_branches(self) -> [str]:
            try:
                branches = []
                a = bindings.drone.drone.getBranches(self.dir)
                for i in range(0, a.size()):
                    branches.append(a.get(i).getName().split("/")[-1])
                return branches
            except:
                return []

        def pull(self, dir, branchName):
            return bindings.pull(dir, branchName)

        def get_current_branch(self, dir):
            return str(bindings.get_full_branch(dir))

        def checkout(self, branchName):
            log.info(f'Change branch to:{branchName}')
            return bindings.drone.drone.checkout(self.dir, branchName)

        def rm_dir(self):
            import shutil
            shutil.rmtree(self.dir)

    Git=_Git('','') #_Git(self.python_root, self.python_root)

    class _FileSystem:
        def get_app_root(self) -> str:
            return str(bindings.android_activity.getFilesDir().toString())
    FileSystem=_FileSystem()
Sdk=_Sdk()
