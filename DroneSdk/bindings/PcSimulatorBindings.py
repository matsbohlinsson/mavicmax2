from pathlib import Path

import cv2

from DroneSdk.bindings.Bindings import Bindings, Telemetry
from simulated_app_root_logs_userdata import get_simulated_app_root

class _SimBindings(Bindings):
    def __init__(self, android_activity):
        super().__init__(android_activity)
        self.android_activity = android_activity

    def get_drone_telemetry(self)-> Telemetry:
        return Telemetry()

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

    def start_simulator(self, lat: float,lon: float):
        self.android_activity.pythonToAndroid.startSimulator(lat,lon)

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
        return get_simulated_app_root() + '/logs/20220101_0101'

    def update_url_touch(self, url:str):
        return self.android_activity.pythonToAndroid.update_url_touch(url)

    def get_key_value(self, keystring:str):
        return self.android_activity.pythonToAndroid.getKeyValue(keystring)

    def set_key_value(self, keystring:str, value):
        self.android_activity.pythonToAndroid.setKeyValue(keystring, value)

    def getBitmapByteArray(self) -> bytearray:
        return bytearray(Path('c:\\tmp/snail.bmp').read_bytes())

    def get_app_root(self) -> str:
        return str("APPROOT")


    def saveFrameToFile(self, filename: str, jpeg_compression: int) -> None:
        print(f"saveFrameToFile:{filename} {jpeg_compression}")

        '''    async def stream_fpv():
                def generate():
                    while True:
                        bitmap = Path('c:\\tmp/snail.bmp').read_bytes()
                        deserialized_bytes = np.frombuffer(bitmap, dtype=np.uint8)
                        #conv = np.reshape(deserialized_bytes, newshape=(256, 256, 4))
                        #conv2 = cv2.cvtColor(conv, cv2.COLOR_BGRA2RGBA)
                        encodedImage = cv2.imencode(".bmp", deserialized_bytes)

                        yield (b'--frame\r\n' b'Content-Type: image/jpg\r\n\r\n' +
                               bytearray(encodedImage) + b'\r\n')
                return StreamingResponse(generate(), media_type="multipart/x-mixed-replace;boundary=frame")
        '''


SimBindings=_SimBindings(None)
