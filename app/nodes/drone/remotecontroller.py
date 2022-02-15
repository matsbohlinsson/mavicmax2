import copy
from dataclasses import dataclass

import MavicMaxGui
import NodeCore
from NodeCore import Node, Event, plugin_name
from NodeCore.test_nodes.nodes import Mover, Generator, Smoother
import DroneSdk
Sdk=DroneSdk.get_drone_sdk()

def create_node(plugin_name=plugin_name(__file__), parent=None):
    return RemoteController(plugin_name=plugin_name, parent=parent)

@dataclass
class Input:
    pass
@dataclass
class Output:
    lx: float = 0.0
    ly: float = 0.0
    rx: float = 0.0
    ry: float = 0.0
    lat: float = 0.0
    lon: float = 0.0
    alt: float = 0.0
    speed : float = 0.0
    baro_alt : float = 0.0
    time : float = 0.0
    acc : float = 0.0


class RemoteController(Node):
    input: Input
    output: Output
    def __init__(self, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)
        self.output.lx = 0.0
        self.output.ly = 0.0
        self.output.rx = 0.0
        self.output.ry = 0.0
        self.output.lat = 0.0
        self.output.lon = 0.0
        self.output.alt = 0.0
        self.output.speed = 0.0
        self.output.baro_alt = 0.0
        self.output.time = 0.0
        self.output.acc = 0.0


    def run(self) -> None:
        Sdk.Rc.update()
        self.output.lx = Sdk.Rc.rc_lx
        self.output.ly = Sdk.Rc.rc_ly
        self.output.rx = Sdk.Rc.rc_rx
        self.output.ry = Sdk.Rc.rc_ry
        self.output.lat = Sdk.Rc.rc_lat
        self.output.lon = Sdk.Rc.rc_lon
        self.output.alt = Sdk.Rc.rc_alt
        self.output.speed = Sdk.Rc.rc_speed
        self.output.baro_alt = Sdk.Rc.rc_baro_alt
        self.output.time = Sdk.Rc.rc_time
        self.output.acc = Sdk.Rc.rc_acc

if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

