from __future__ import annotations
import logging
from dataclasses import dataclass, field
from NodeCore import Event, General, plugin_name
from statistics import mean


def main_loop(input: Input, output: Output, log: logging.Logger) -> None:
    output.value_history = input.value_history.copy()
    output.value_history.append(input.value)
    output.value_history = output.value_history[-int(input.window_size):]
    speed_avg = mean(output.value_history)
    output.value = speed_avg if abs(input.value - speed_avg) < input.delta_max else input.value


class Smoother(General):
    input: Input
    output: Output


@dataclass
class Input:
    value_history: [float] = field(default_factory=list)
    stop: Event = field(default_factory=Event)
    value: float = 0
    delta_max: float = 4
    window_size: int = 3


@dataclass
class Output:
    value: float = 0
    value_history:  [float] = field(default_factory=list)

def reset_history(input: Input, output: Output) -> None:
    input.value_history=[]

def init(input: Input, output: Output, log: logging.Logger) -> None:
    input.stop.register(lambda : reset_history(input, output))

def feedback_loop(input: Input, output: Output, log: logging.Logger) -> None:
    input.value_history = output.value_history.copy()

def create_node(plugin_name=plugin_name(__file__), parent=None) -> Smoother:
    return Smoother(plugin_name=plugin_name, init=init, run=main_loop, run_post=feedback_loop, parent=parent, input=Input(), output=Output())


if __name__ == "__main__":
    import NodeCore
    NodeCore.run_from_main(__file__)

