import dataclasses
import time
from abc import ABC

from NodeCore import Node


@dataclasses.dataclass
class NodeRunner():
    node: Node
    loop_delay_ms: int = 100
    running = bool = True
    loop_nbr:int  = 0

    def start(self):
        self.running = True
        self.loop()

    def stop(self):
        self.loop()
        self.running = False

    def loop(self):
        while self.running:
            print(f"loop:{Node.clock_tick}")
            self.node.execute_node()
            time.sleep(self.loop_delay_ms/1000)
            Node.clock_tick = Node.clock_tick +1


if __name__ == "__main__":
    import test_nodes.nodes.Generator
    node = test_nodes.nodes.Generator.create_node()
    runner=NodeRunner(node=node, loop_delay_ms=200)
    runner.start()
