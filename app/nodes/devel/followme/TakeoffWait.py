import logging
from dataclasses import dataclass
from datetime import datetime
import app.util

import NodeCore
from NodeCore import Node, Event, plugin_name
import DroneSdk.sdk as sdk

def create_node(plugin_name=plugin_name(__file__), parent=None):
    return TakeoffWait(plugin_name=plugin_name, parent=parent)

@dataclass
class Input:
    lat1: float = 58.00004
    lon1: float = 11.00003
    lat2: float = 58.00002
    lon2: float = 11.00001
    distance: int = 200

@dataclass
class Output:
    takeoff: bool = False
    distance: int = 0


class TakeoffWait(Node):
    input: Input
    output: Output
    def __init__(self, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)

    def run(self) -> None:
        i = self.input
        loc1 = app.util.Location(i.lat1, i.lon1)
        loc2 = app.util.Location(i.lat2, i.lon2)
        self.output.distance = int(loc1.distance_to(loc2))
        if self.output.distance > i.distance:
            self.output.takeoff = True
        else:
            self.output.takeoff = False


if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

