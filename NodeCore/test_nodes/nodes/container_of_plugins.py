from dataclasses import dataclass

import NodeCore
from NodeCore import Node, Event, plugin_name
from NodeCore.test_nodes.nodes import Mover, Generator, Smoother


def create_node(plugin_name=plugin_name(__file__), parent=None):
    return Container_of_plugins(plugin_name=plugin_name, parent=parent)

@dataclass
class Input:
    stop_event: float = Event()
    speed: float = 0

@dataclass
class Output:
    stop_event: float = Event()
    speed: float = 0
    height: float = 0

class Container_of_plugins(Node):
    input: Input
    output: Output
    def __init__(self, *args, **kwargs) -> None:
        input, output = Input(stop_event=1), Output(stop_event=2)
        super().__init__(input=input, output=output, *args, **kwargs)
        self.smoother = Smoother.create_node(parent=self)
        self.mover = Mover.create_node(parent=self)
        self.generator = Generator.create_node(parent=self)

    def run(self) -> None:
        self.smoother.input.value = self.input.speed
        self.smoother.execute_node()
        self.generator.execute_node()

        self.mover.input.speed = self.smoother.output.value
        self.mover.input.height = self.generator.output.value
        self.mover.execute_node()

        self.output.speed = self.mover.output.speed
        self.output.height = self.mover.output.height

        if self.input.speed==2.0: self.log_buffer.write("speed_2")


if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

