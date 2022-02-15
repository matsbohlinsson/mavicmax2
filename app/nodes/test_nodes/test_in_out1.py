from dataclasses import dataclass
from enum import Enum

import MavicMaxGui
import NodeCore
from DroneSdk.dji.DjiKeys import Keys
from NodeCore import Node, plugin_name
import DroneSdk
from MavicMaxGui import Select

Sdk=DroneSdk.get_drone_sdk()

def create_node(plugin_name=plugin_name(__file__), parent=None):
    '''
        Only used for testing pruposes
    '''
    return FlightController(plugin_name=plugin_name, parent=parent)


@dataclass
class Input:
    class Select(Enum):
        SPORT=1
        MANUAL = 2
        GPS = 3

    speed_x: float = 1.0
    speed_y: float = 12.0
    select: int = 1

    _speed_x: MavicMaxGui.Slider = MavicMaxGui.Slider(default_value=0, min=0, max=10, step=0.1)
    _select: MavicMaxGui.SelectTextbox = MavicMaxGui.Selectbox(choice_dict={i.name: i.value for i in Select})

    keys: str = ""
    _keys: MavicMaxGui.SelectTextbox = MavicMaxGui.Selectbox(choice_dict={i.name: i.value for i in Keys.FlightController})



@dataclass
class Output:
    speed_x: float = 0.0
    message_screen: str = "NoTextYet"
    selected: str = ''


class FlightController(Node):
    input: Input
    output: Output
    i: int =0
    def __init__(self, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)

    def run(self) -> None:
        self.output.speed_x = self.input.speed_x+0.1
        self.input.speed_x = self.output.speed_x + 0.1
        if self.input.speed_x>10:
            self.output.message_screen = f'Zero:{self.i}'
            self.input._select.append(f'Zero:{self.i}', f'Zero:{self.i}')
            self.i=self.i+1
            self.input.speed_x = 0
        self.output.selected = self.input.select


if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

