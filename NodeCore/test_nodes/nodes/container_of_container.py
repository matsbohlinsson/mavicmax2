from dataclasses import dataclass
from NodeCore import Node, plugin_name
from NodeCore.test_nodes.nodes.container_of_plugins import Container_of_plugins

def create_node(plugin_name=plugin_name(__file__), parent=None):
    return Container_of_container(plugin_name=plugin_name, parent=parent)

@dataclass
class Input:
    speed: float = 0

@dataclass
class Output:
    speed: float = 0
    height: float = 0


class Container_of_container(Node):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(input=Input(), output=Output(), *args, **kwargs)
        self.container_of_plugins1 = Container_of_plugins(parent=self, plugin_name='Container_of_plugins1')

    def run(self) -> None:
        #In
        self.container_of_plugins1.input.speed = self.input.speed
        # Execute
        self.container_of_plugins1.execute_node()
        #Out
        self.output.speed = self.container_of_plugins1.output.speed
        self.output.height = self.container_of_plugins1.output.height

if __name__ == "__main__":
    import NodeCore
    NodeCore.run_from_main(__file__)
