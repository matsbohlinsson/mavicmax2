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
class FloatMaxMinStep:
    value: float = 0
    min: float = 0
    max: float = 10
    step: float = 0.1

    def get_ui(self):
        return MavicMaxGui.Slider(default_value=0, min=self.min, max=self.max, step=self.step)
    def get(self):
        return self.value
    def set(self, value):
        self.value = value

class MySelect(Enum):
    SPORT=1
    MANUAL = 2
    GPS = 3

@dataclass
class IntEnum:
    value: int = 0
    step: float = 0.1

    def get_ui(self):
        return MavicMaxGui.Selectbox(choice_dict={i.name: i.value for i in MySelect})
    def get(self):
        return self.value
    def set(self, value):
        self.value = value


@dataclass
class Input:

    speed_x: float = 1.0
    speed_y: MavicMaxGui.FloatMaxMinStep = MavicMaxGui.FloatMaxMinStep(0.0, 0.0, 15.0, 0.1)
    select:  MavicMaxGui.SelectEnum = MavicMaxGui.SelectEnum(0, MySelect)
    myfloat: FloatMaxMinStep = FloatMaxMinStep(0.0, 0.0, 10, 0.1)
    myIntEnum: FloatMaxMinStep = IntEnum(0, 0)
    keys: MavicMaxGui.SelectEnum = MavicMaxGui.SelectEnum(0, Keys.FlightController)



@dataclass
class Output:
    speed_x: float = 0.0
    message_screen: str = "NoTextYet"
    selected: str = ''
    mytest_out: str = "nada"


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
            #self.input.select.append(f'Zero:{self.i}', f'Zero:{self.i}') #Implement append or inherit
            self.i=self.i+1
            self.input.speed_x = 0
        self.output.selected = self.input.select
        self.output.mytest_out = self.input.myfloat.get()
        self.input.speed_y.set(self.output.speed_x)


if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

