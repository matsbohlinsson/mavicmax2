import copy
import logging
from dataclasses import dataclass
from datetime import datetime

import MavicMaxGui
import NodeCore
from NodeCore import Node, Event, plugin_name
from NodeCore.test_nodes.nodes import Mover, Generator, Smoother
import DroneSdk
Sdk=DroneSdk.get_drone_sdk()

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
            Sdk.Telemetry.update()
            today = datetime.now()
            self.output.time = today.strftime("%H:%M:%S.%f")[:-5]
            self.output.speed_x = Sdk.Telemetry.speed_x
            self.output.speed_y = Sdk.Telemetry.speed_y
            self.output.speed_z = Sdk.Telemetry.speed_z
            self.output.yaw = Sdk.Telemetry.yaw
            self.output.pitch = Sdk.Telemetry.pitch
            self.output.roll = Sdk.Telemetry.roll
            self.output.lat = Sdk.Telemetry.lat
            self.output.lon = Sdk.Telemetry.lon
            self.output.height = Sdk.Telemetry.height
            self.output.is_flying = Sdk.Telemetry.isFlying
            self.output.gps_level = Sdk.Telemetry.gps_level
            self.output.flight_mode = Sdk.Telemetry.flight_mode
            self.output.drone_type = Sdk.Telemetry.drone_type
            self.output.terrain_height = Sdk.Telemetry.terrain_height
            self.output.rpm = Sdk.Telemetry.rpm
            self.output.motor_on_nbr = Sdk.Telemetry.motor_on_nbr
            self.output.flytime = Sdk.Telemetry.flytime
            self.output.state = Sdk.Telemetry.state
            self.output.speed_xy = Sdk.Telemetry.speed_xy
            self.output.course = Sdk.Telemetry.course

            self.output.keytest =  Sdk.Keys.get(Sdk.Keys.Key.FlightController.ATTITUDE_YAW)
            self.output.key2test =  Sdk.Keys.get(Sdk.Keys.Key.FlightController.GO_HOME_HEIGHT_IN_METERS)

        except:
            logging.exception('Telemetry')





if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

