import copy
from dataclasses import dataclass

import MavicMaxGui
import NodeCore
from NodeCore import Node, Event, plugin_name
from NodeCore.test_nodes.nodes import Mover, Generator, Smoother

def create_node(plugin_name=plugin_name(__file__), parent=None):
    '''
        Only used for testing pruposes
    '''
    return FlightController(plugin_name=plugin_name, parent=parent)

@dataclass
class Input:
    speed_x2: float = 1.0
    pass
@dataclass
class Output:
    speed_x2: float = 0.0


class FlightController(Node):
    input: Input
    output: Output
    def __init__(self, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)

    def run(self) -> None:
        self.output.speed_x2 = self.output.speed_x2+0.1
        self.input.speed_x2 = self.output.speed_x2 + 0.1

if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

