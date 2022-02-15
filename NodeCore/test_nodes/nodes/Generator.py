from __future__ import annotations
import math
import logging
from dataclasses import dataclass
from typing import Callable

from NodeCore import General, plugin_name

class Generator(General):
    input: Input
    output: Output

@dataclass
class Input:
    start_value: float = 0
    function: Callable[[float], float] = None

@dataclass
class Output:
    value: float = 0


def init(input: Input, output: Output, log: logging.Logger) -> None:
    input.function = lambda x: math.sin(x / 100) * 100

def main_loop(input: Input, output: Output, log: logging.Logger) -> None:
    output.value = input.function(input.start_value)

def feedback_loop(input: Input, output: Output, log: logging.Logger) -> None:
    input.start_value = input.start_value+1


def create_node(plugin_name=plugin_name(__file__), parent=None) -> Generator:
    return Generator(plugin_name=plugin_name, init=init, run_post=feedback_loop, run=main_loop, parent=parent, input=Input(), output=Output())


if __name__ == "__main__":
    import NodeCore
    NodeCore.run_from_main(__file__)




