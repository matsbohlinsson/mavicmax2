import copy
from dataclasses import dataclass

import MavicMaxGui
import NodeCore
from NodeCore import Node, Event, plugin_name
from NodeCore.test_nodes.nodes import Mover, Generator, Smoother
import DroneSdk
Sdk=DroneSdk.get_drone_sdk()

def create_node(plugin_name=plugin_name(__file__), parent=None):
    '''
        Only used for testing pruposes
    '''
    return FlightController(plugin_name=plugin_name, parent=parent)

@dataclass
class Integer:
    value: int = 0

    def get(self):
        return self.value

    def set(self, value:int):
        self.value = value


@dataclass
class Input:
    speed_xx: Integer = Integer(1)
    pass
@dataclass
class Output:
    speed_out: int = 73
    speed_x: Integer = Integer(1)


class FlightController(Node):
    input: Input
    output: Output
    def __init__(self, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)

    def run(self) -> None:
        self.output.speed_x.set(self.input.speed_xx.get()+1)
        self.input.speed_xx.set(self.input.speed_xx.get()+1)

if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

