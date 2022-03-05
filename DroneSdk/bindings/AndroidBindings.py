import math

from DroneSdk import models
from DroneSdk.bindings.Bindings import Bindings

try:
    from java import dynamic_proxy, jboolean, jvoid, Override, static_proxy
    from android.app import AlertDialog
    from android.content import Context, DialogInterface
    from dji.sdk.products import Aircraft
    from dji.keysdk import FlightControllerKey
    from java.lang import Runnable
    from android.widget import Toast
    from com.plainembedded.mavicmax.drone import DjiValuesCache
    from com.plainembedded.mavicmax.drone import Common
    from com.plainembedded.mavicmax.ui import CommonUI
    from com.plainembedded.mavicmax.drone import DroneMover
except:
    pass

from sys import platform
try:
    class myrunnable(dynamic_proxy(Runnable)):
        def __init__(self, func):
            super().__init__()
            self.func = func
        def run(self):
            self.func()
except:
    pass


def calc_course(x: float, y: float):
    r = math.sqrt(x ** 2 + y ** 2)
    theta = math.atan2(y, x)
    degrees = math.degrees(theta)
    if degrees < 0:
        degrees += 360
    return degrees


class _DjiBindings(Bindings):
    def __init__(self, android_activity):
        super().__init__(android_activity)
        self.android_activity = android_activity

    def get_drone_telemetry(self) -> models.Telemetry:
        djitelemtry =  self.android_activity.pythonToAndroid.getTelemetry()
        telemtry = models.Telemetry(
            speed_x = djitelemtry.getXSpeed() / 10.0,
            speed_y = djitelemtry.getYSpeed() / 10.0,
            speed_z = djitelemtry.getZSpeed() / 10.0,
            yaw = djitelemtry.getYaw() / 10.0,
            pitch = djitelemtry.getPitch() / 10.0,
            roll = djitelemtry.getRoll() / 10.0,
            lat = djitelemtry.getLatitude(),
            lon = djitelemtry.getLongitude(),
            height = djitelemtry.getHeight() / 10.0,
            is_flying = djitelemtry.groundOrSky(),
            gps_number = djitelemtry.getGpsNum(),
            gps_level = djitelemtry.getGpsLevel(),
            flight_mode = str(djitelemtry.getFlightAction()),
            drone_type = str(djitelemtry.getDroneType()),
            terrain_height = djitelemtry.getSwaveHeight() / 10.0,
            motor_on_nbr = djitelemtry.getMotorRevolution(),
            rpm = -11,  # telemetry.getEscAverageSpeed() dji.midware.data.model.P3.DataFlycGetPushPowerParam.getInstance().getEscAverageSpeed();
            flytime = djitelemtry.getFlyTime(),
            state = str(djitelemtry.getFlycState()),
            speed_xy = round(math.sqrt(djitelemtry.speed_x ** 2 + djitelemtry.speed_y ** 2), 1),
            course = round(calc_course(djitelemtry.speed_x, djitelemtry.speed_y), 1)
        )
        return telemtry

    def start_simulator(self, lat: float,lon: float):
        self.android_activity.pythonToAndroid.startSimulator(lat,lon)

    def stop_simulator(self):
        self.android_activity.pythonToAndroid.stop()


    def start_virtual_sticks(self):
        self.android_activity.pythonToAndroid.startVirtualStickRaw()

    def stop_virtual_sticks(self):
        self.android_activity.pythonToAndroid.stopVirtualStickRaw()

    def send_virtual_stick_raw(self, flag, throttle, roll, pitch, yaw, duration):
        self.android_activity.pythonToAndroid.sendVirtualStickRaw(int(flag), float(throttle), float(roll), float(pitch), float(yaw), int(duration) * 1000)

    def start_motors(self):
        self.android_activity.pythonToAndroid.startMotors()

    def restart_app(self):
        self.android_activity.pythonToAndroid.restartApp()


    def takeoff(self):
        self.android_activity.pythonToAndroid.takeoff()

    def force_boost(self):
        self.android_activity.pythonToAndroid.forceBoost()

    def start_record(self):
        self.android_activity.pythonToAndroid.startRecord()

    def stop_record(self):
        self.android_activity.pythonToAndroid.stopRecord()

    def start_photo(self):
        self.android_activity.pythonToAndroid.startPhoto()

    def stop_photo(self):
        self.android_activity.pythonToAndroid.stopPhoto()

    def beep(self, index: int=1, freq: int=93 , durationMs: int=100, silentMs: int=100, loop: int=1):
        self.android_activity.pythonToAndroid.beep(index, freq, durationMs, silentMs, loop)

    def show_toast(self, text="No Message"):
        self.android_activity.runOnUiThread(myrunnable(lambda : Toast.makeText(self.android_activity, text,Toast.LENGTH_SHORT).show()))

    def init(self, android_activity):
        self.android_activity = android_activity

    def pull(self, dir, branchName) -> str:
        return str(self.android_activity.pythonToAndroid.pull(dir, branchName))

    def get_full_branch(self, dir):
        branch =  str(self.android_activity.pythonToAndroid.getFullBranch(dir))
        return branch

    def get_rc_inputs(self):
        a = self.android_activity.pythonToAndroid.getRemoteInputs()
        return a

    def get_rc_gps(self):
        a = self.android_activity.pythonToAndroid.getRemoteGps()
        return a

    def get_log_dir(self):
        return self.android_activity.pythonToAndroid.getLogDir()

    def update_url_touch(self, url:str):
        return self.android_activity.pythonToAndroid.update_url_touch(url)

    def get_key_value(self, keystring:str):
        return self.android_activity.pythonToAndroid.getKeyValue(keystring)

    def set_key_value(self, keystring:str, value):
        self.android_activity.pythonToAndroid.setKeyValue(keystring, value)
DjiBindings=_DjiBindings(None)

