import dataclasses
from abc import ABC, abstractmethod

from DroneSdk.models import Telemetry


class Bindings(ABC):
    def __init__(self, android_activity):
        self.android_activity = android_activity

    @abstractmethod
    def get_drone_telemetry(self) -> Telemetry:
        return Telemetry()
        pass
    @abstractmethod
    def start_virtual_sticks(self):
        pass

    @abstractmethod
    def stop_virtual_sticks(self):
        pass

    @abstractmethod
    def send_virtual_stick_raw(self, flag, throttle, roll, pitch, yaw, duration):
        pass

    @abstractmethod
    def start_motors(self):
        pass

    @abstractmethod
    def restart_app(self):
        pass

    @abstractmethod
    def start_simulator(self, lat: float,lon: float):
        pass

    @abstractmethod
    def takeoff(self):
        pass

    @abstractmethod
    def force_boost(self):
        pass

    @abstractmethod
    def start_record(self):
        pass

    @abstractmethod
    def stop_record(self):
        pass

    @abstractmethod
    def start_photo(self):
        pass

    @abstractmethod
    def stop_photo(self):
        pass

    @abstractmethod
    def beep(self, index: int=1, freq: int=93 , durationMs: int=100, silentMs: int=100, loop: int=1):
        pass

    @abstractmethod
    def show_toast(self, text="No Message"):
        pass

    @abstractmethod
    def init(self, android_activity):
        pass

    @abstractmethod
    def pull(self, dir, branchName) -> str:
        pass

    @abstractmethod
    def get_full_branch(self, dir):
        pass

    @abstractmethod
    def get_rc_inputs(self):
        pass

    @abstractmethod
    def get_rc_gps(self):
        pass

    @abstractmethod
    def get_log_dir(self):
        pass

    @abstractmethod
    def update_url_touch(self, url:str):
        pass

    @abstractmethod
    def get_key_value(self, keystring:str):
        pass

    @abstractmethod
    def set_key_value(self, keystring:str, value):
        pass
