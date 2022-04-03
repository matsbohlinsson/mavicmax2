import logging
from dataclasses import dataclass
from datetime import datetime
import app.util

import NodeCore
from NodeCore import Node, Event, plugin_name
import DroneSdk.sdk as sdk

def create_node(plugin_name=plugin_name(__file__), parent=None):
    return Follower(plugin_name=plugin_name, parent=parent)

@dataclass
class Input:
    target_course: float = 0.0
    target_speed: float = 0.0
    distance: float = 0.0
    bearing: float = 0.0
    speed: float = 0.0
    k_distance: float = 0.2

@dataclass
class Output:
    course:float = 0.0
    speed:float = 0.0

class Follower(Node):
    input: Input
    output: Output
    def __init__(self, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)

    def run(self) -> None:
        self.output.speed = self.input.distance * self.input.k_distance + self.input.target_speed




if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

