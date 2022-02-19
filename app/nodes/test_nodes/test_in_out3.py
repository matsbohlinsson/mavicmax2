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



class MySelect(Enum):
    ONE=1
    TWO = 2
    THREE = 3


class MySelect2(Enum):
    ONE=1
    TWO = 2
    THREE = 3
    FOUR = 4
    FIVE = 5



@dataclass
class Input:
    select: int = 1
    myfloat: MavicMaxGui.FloatMaxMinStep = MavicMaxGui.FloatMaxMinStep(0.0, 0.0, 10.0, 0.1)
    myIntEnum: MavicMaxGui.SelectEnum = MavicMaxGui.SelectEnum(0, MySelect2)
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

