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
    value: float = 0.0
    min: float = 0.0
    max: float = 10.0
    step: float = 0.1

    def get_ui(self):
        return MavicMaxGui.Slider(default_value=0.0, min=self.min, max=self.max, step=self.step)
    def get(self):
        return self.value
    def set(self, value):
        self.value = value

class MySelect(Enum):
    ONE=1
    TWO = 2
    THREE = 3

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

    select: int = 1
    myfloat: FloatMaxMinStep = FloatMaxMinStep(0.0, 0.0, 10.0, 0.1)
    myIntEnum: FloatMaxMinStep = IntEnum(0, 0)
    _speed_x: MavicMaxGui.Slider = MavicMaxGui.Slider(default_value=0, min=0, max=10, step=0.1)
    _select: MavicMaxGui.SelectTextbox = MavicMaxGui.Selectbox(choice_dict={i.name: i.value for i in MySelect})



@dataclass
class Output:
    selected: str = ''
    mytest_out: str = 'XX'
    myfloat_out: float = 73.73


class FlightController(Node):
    input: Input
    output: Output
    i: int =0
    def __init__(self, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)

    def run(self) -> None:
        self.output.selected = self.input.select
        self.output.mytest_out = self.input.myIntEnum.get()
        self.output.myfloat_out = self.input.myfloat.get()


if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

