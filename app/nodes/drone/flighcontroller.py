import copy
import logging
from dataclasses import dataclass, field

import DroneSdk
#import DroneSdk.DroneSimulator as DroneSdk
import MavicMaxGui
import NodeCore
from NodeCore import Node, Event, plugin_name
from NodeCore.test_nodes.nodes import Mover, Generator, Smoother
from DroneSdk.Sdk_old import Sdk
log = logging.getLogger(__file__)

def create_node(plugin_name=plugin_name(__file__), parent=None):
    return FlightController(plugin_name=plugin_name, parent=parent)

@dataclass
class Input:
    start_flying: bool = False
    height: float = 0
    course: float = 0
    speed: float = 0
    heading: float=0
    rth: bool=False
    # Constraints
    height_low_limit:float = 1.0
    speed_limit = 15
    start_sim: Event = field(default_factory=Event)

@dataclass
class Output:
    dummy:int=1
    pass

class FlightController(Node):
    input: Input
    output: Output
    def __init__(self, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)
        self.input.start_sim.register(lambda: Sdk.Flightctrl.start_simulator())
        #self.input_old = copy.deepcopy(self.input)

    def run(self) -> None:
        try:
            i = self.input
            if self.input.start_flying:
                Sdk.Flightctrl.start_motors()
                Sdk.Flightctrl.set_speed(course=i.course, speed=i.speed, height=i.height, heading=i.heading)

        except:
            log.exception("telemetry")

if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

