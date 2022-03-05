import logging
from dataclasses import dataclass, field
import NodeCore
from NodeCore import Node, Event, plugin_name
import DroneSdk.sdk as sdk
log = logging.getLogger(__file__)

def create_node(plugin_name=plugin_name(__file__), parent=None):
    return FlightController(plugin_name=plugin_name, parent=parent)

@dataclass
class Input:
    kill_switch: int = 0
    height: float = 0
    course: float = 0
    speed: float = 0
    heading: float=0
    rth: bool=False
    # Constraints
    height_low_limit:float = 1.0
    speed_limit = 15
    start_sim: Event = field(default_factory=Event)
    takeoff: Event = field(default_factory=Event)
    start_motors: Event = field(default_factory=Event)
    virtualstick_on: Event = field(default_factory=Event)

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
        self.input.start_sim.register(sdk.start_simulator)
        self.input.start_motors.register(sdk.start_motors)
        self.input.takeoff.register(sdk.takeoff)
        self.input.virtualstick_on.register(sdk.start_virtual_sticks)

    def run(self) -> None:
        try:
            i = self.input
            if i.kill_switch:
                sdk.set_speed(course=i.course, speed=i.speed, height=i.height, heading=i.heading, duration=0.2)
        except:
            log.exception("flightcontroller")

if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

