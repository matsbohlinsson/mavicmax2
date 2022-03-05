import logging
from dataclasses import dataclass
from datetime import datetime

import NodeCore
from NodeCore import Node, Event, plugin_name
import DroneSdk.sdk as sdk

def create_node(plugin_name=plugin_name(__file__), parent=None):
    return Telemetry(plugin_name=plugin_name, parent=parent)

@dataclass
class Input:
    update_rate_ms: int = 100
@dataclass
class Output:
    speed_x: float = 0.0
    speed_y: float = 0.0
    speed_z: float = 0.0
    speed_xy:float = 0.0
    course:float = 0.0
    yaw: float = 0.0
    pitch: float = 0.0
    roll: float = 0.0
    lat: float = 12.11111111
    lon: float = 13.11111111
    height: float = 0.0
    is_flying: int = 0.0
    gps_level: int=-1
    flight_mode: str='xxxxxxxxx'
    drone_type: str='xxxxxxxxx'
    terrain_height: float=-1.0
    motor_on_nbr: int=-1
    rpm: int=-1
    flytime:int= -1
    state:str = 'xxxxxxxxx'
    time: str = ''



class Telemetry(Node):
    input: Input
    output: Output
    def __init__(self, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)

    def run(self) -> None:
        try:
            telemetry = sdk.get_drone_telemetry()
            today = datetime.now()
            self.output.time = today.strftime("%H:%M:%S.%f")[:-5]
            self.output.speed_x = telemetry.speed_x
            self.output.speed_y = telemetry.speed_y
            self.output.speed_z = telemetry.speed_z
            self.output.yaw = telemetry.yaw
            self.output.pitch = telemetry.pitch
            self.output.roll = telemetry.roll
            self.output.lat = telemetry.lat
            self.output.lon = telemetry.lon
            self.output.height = telemetry.height
            self.output.is_flying = telemetry.is_flying
            self.output.gps_level = telemetry.gps_level
            self.output.flight_mode = telemetry.flight_mode
            self.output.drone_type = telemetry.drone_type
            self.output.terrain_height = telemetry.terrain_height
            self.output.rpm = telemetry.rpm
            self.output.motor_on_nbr = telemetry.motor_on_nbr
            self.output.flytime = telemetry.flytime
            self.output.state = telemetry.state
            self.output.speed_xy = telemetry.speed_xy
            self.output.course = telemetry.course
            #self.output.keytest =  Sdk.Keys.get(Sdk.Keys.Key.FlightController.ATTITUDE_YAW)
            #self.output.key2test =  Sdk.Keys.get(Sdk.Keys.Key.FlightController.GO_HOME_HEIGHT_IN_METERS)
        except:
            logging.exception('Telemetry')


if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

