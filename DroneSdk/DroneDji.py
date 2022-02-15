import dataclasses
import logging
import math

import DroneSdk.AndroidBindings
from DroneSdk.dji import DjiKeys

log = logging.getLogger(__file__)

class Sdk:
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
        def __init__(self):
            self.api = DroneSdk.AndroidBindings.DjiBindings
        def restart_app(self):
            self.api.restart_app()

        def get_log_dir(self):
            return self.api.get_log_dir()

    Admin=_Admin()

    class _Ui:
        def __init__(self):
            self.api = DroneSdk.AndroidBindings.DjiBindings
        def update_url_touch(self, url:str):
            self.api.update_url_touch(url)
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
            def rawstick_to_float(value) -> float:
                value = float(value)
                return round((value - 1024) / 660, 4)

            try:
                rc_gps = self.api.get_rc_gps()
                self.rc_lat = rc_gps[0]
                self.rc_lon = rc_gps[1]
                self.rc_alt = rc_gps[2]
                self.rc_speed = rc_gps[3]
                self.rc_baro_alt = rc_gps[4]
                self.rc_time = rc_gps[5]
                self.rc_acc = rc_gps[6]
                rc_sticks = self.api.get_rc_inputs()
                self.rc_lx = rawstick_to_float(rc_sticks[0])
                self.rc_ly = rawstick_to_float(rc_sticks[1])
                self.rc_rx = rawstick_to_float(rc_sticks[2])
                self.rc_ry = rawstick_to_float(rc_sticks[3])

            except:
                log.exception("telemetry")
    Rc=_Rc()

    class _Flightcontroller:

        def __init__(self):
            self.api = DroneSdk.AndroidBindings.DjiBindings

        def start_motors(self):
            self.api.start_motors()

        def take_off(self):
            self.api.take_off()

        def set_speed(self, course: float = None, speed: float = 0, height: float = None, heading: float = None, duration:float=1.5):
            flag = Sdk.Helpers.getVirtualstickRawFlag(advanced=1, body=0, yawSpeed=0, vertAltitude=1, pitchSpeed=1)
            radBearing = math.radians(course)
            pitch = speed * math.cos(radBearing)
            roll = speed * math.sin(radBearing)
            yaw = heading
            self.api.send_virtual_stick_raw(flag=flag, throttle=height, roll=roll, pitch=pitch, yaw=yaw, duration=duration)

        def start_simulator(self, lat: float=58.11111,lon: float = 11.1111111):
            self.api.start_simulator(lat, lon)
    Flightctrl=_Flightcontroller()

    @dataclasses.dataclass
    class _Telemetry:
        speed_x: float = 0
        speed_y: float = 0
        speed_z: float = 0
        yaw: float = 0
        pitch: float = 0
        roll: float = 0
        lat: float = 0
        lon: float = 0
        height: float = 0
        isFlying: int = 0
        gps_lev: int=-1
        flight_mode: str=''
        drone_type: str=''
        terrain_height: float=-1.0
        rpm: int=-1
        flytime:int= -1
        state:str = ''
        speed_xy: float = 0.0
        course: float = 0.0

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
            self.api = DroneSdk.AndroidBindings.DjiBindings

        def update(self):
            try:
                self.telemetry = self.api.get_telemetry()
                self.speed_x = self.telemetry.getXSpeed()/10.0
                self.speed_y = self.telemetry.getYSpeed()/10.0
                self.speed_z = self.telemetry.getZSpeed()/10.0
                self.yaw = self.telemetry.getYaw()/10.0
                self.pitch = self.telemetry.getPitch()/10.0
                self.roll = self.telemetry.getRoll()/10.0
                self.lat = self.telemetry.getLatitude()
                self.lon = self.telemetry.getLongitude()
                self.height = self.telemetry.getHeight()/10.0
                self.isFlying = self.telemetry.groundOrSky()

                self.getGpsNum = self.telemetry.getGpsNum()
                self.gps_level = self.telemetry.getGpsLevel()
                self.flight_mode = str(self.telemetry.getFlightAction())
                self.drone_type = str(self.telemetry.getDroneType())
                self.terrain_height = self.telemetry.getSwaveHeight() / 10.0
                self.motor_on_nbr = self.telemetry.getMotorRevolution()
                self.rpm = -11 #self.telemetry.getEscAverageSpeed() dji.midware.data.model.P3.DataFlycGetPushPowerParam.getInstance().getEscAverageSpeed();
                self.flytime = self.telemetry.getFlyTime()
                self.state = str(self.telemetry.getFlycState())
                self.speed_xy = round(math.sqrt(self.speed_x**2 + self.speed_y**2),1)
                self.course = round(self.calc_course(self.speed_x, self.speed_y),1)
            except:
                log.exception("telemetry")

        def calc_course(self, x:float,y:float):
            r = math.sqrt(x**2 + y**2)
            theta = math.atan2(y, x)
            degrees = math.degrees(theta)
            if degrees < 0:
                degrees += 360
            return degrees




            '''
            self. = self.telemetry.
            groundOrSky()
            sMotorUp()
            isSwaveWork()
            getGohomeStatus()
            isVisionUsed()
            getVoltageWarning()
            getModeChannel()
            getModeChannelByFR()
            isGpsUsed()
            getCompassError()
            getGpsLevel()
            getBatteryType()
            isGPSValid()
            getGpsNum()
            getFlightAction()

            getRcState()
            getFlycState()
            getAppCommand()
            canIOCWork()
            getSwaveHeight()
            getFlyTime()
            getMotorRevolution()
            getFlycVersion()
            getDroneType()
            isTakeoffFail()
            getWindSpeed()
            getWindDirection()
            '''

    Telemetry=_Telemetry()


    class _Keys:
        Key=DjiKeys.Keys
        def __init__(self):
            self.api = DroneSdk.AndroidBindings.DjiBindings

        def get(self, key:Key):
            return self.api.get_key_value(key.value)
        def set(self, key:Key, value):
            return self.api.set_key_value(key.value, value)
    Keys=_Keys()

    class _Git:
        def __init__(self, dir:str, url:str):
            self.dir=dir
            self.url=url
            self.api = DroneSdk.AndroidBindings.DjiBindings

        def clone(self, dir, url):
            self.api.drone.drone.clone(dir, url, "", "")

        def diff(self):
            self.api.drone.drone.diff(self.dir)

        def commit_all(self, message='From app'):
            self.api.drone.drone.commit_all(self.dir, message)

        def status(self):
            return self.api.drone.drone.status(self.dir)

        def log(self):
            return "Not impl"

        def get_branches(self) -> [str]:
            try:
                branches = []
                a = self.api.drone.drone.getBranches(self.dir)
                for i in range(0, a.size()):
                    branches.append(a.get(i).getName().split("/")[-1])
                return branches
            except:
                return []

        def pull(self, dir, branchName):
            return self.api.pull(dir, branchName)

        def get_current_branch(self, dir):
            return str(self.api.get_full_branch(dir))

        def checkout(self, branchName):
            log.info(f'Change branch to:{branchName}')
            return self.api.drone.drone.checkout(self.dir, branchName)

        def rm_dir(self):
            import shutil
            shutil.rmtree(self.dir)



    Git=_Git('','') #_Git(self.python_root, self.python_root)

    class _FileSystem:
        def __init__(self):
            self.api = DroneSdk.AndroidBindings.DjiBindings

        def get_app_root(self) -> str:
            return str(self.api.android_activity.getFilesDir().toString())
    FileSystem=_FileSystem()
Sdk=Sdk()
