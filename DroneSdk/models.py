import dataclasses
from enum import Enum


@dataclasses.dataclass
class Telemetry:
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
    gps_number: int = -1
    gps_level: int = -1
    flight_mode: str = 'xxxxxxxxx'
    drone_type: str = 'xxxxxxxxx'
    terrain_height: float = -1.0
    motor_on_nbr: int = -1
    rpm: int = -1
    flytime: int = -1
    state: str = 'xxxxxxxxx'
    time: str = ''


@dataclasses.dataclass
class Rc:
    lx: float = 0.0
    ly: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    lat: float = 0.0
    lon: float = 0.0
    alt: float = 0.0
    speed : float = 0.0
    baro_alt : float = 0.0
    time : float = 0.0
    acc : float = 0.0

