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
    input.function = lambda x: math.cos(x / 100) * 100

def main_loop(input: Input, output: Output, log: logging.Logger) -> None:
    output.value = input.function(input.start_value)

def feedback_loop(input: Input, output: Output, log: logging.Logger) -> None:
    input.start_value = input.start_value+1


def create_node(plugin_name=plugin_name(__file__), parent=None) -> Generator:
    return Generator(plugin_name=plugin_name, init=init, run_post=feedback_loop, run=main_loop, parent=parent, input=Input(), output=Output())


testdata = [{'clock_tick': 0.0, 'input.start_value': 0.0, 'output.value': 0.0, 'log': '', 'Generator.py': ''}, {'clock_tick': 1.0, 'input.start_value': 1.0, 'output.value': 0.9999833334166665, 'log': '', 'Generator.py': ''}, {'clock_tick': 2.0, 'input.start_value': 2.0, 'output.value': 1.999866669333308, 'log': '', 'Generator.py': ''}, {'clock_tick': 3.0, 'input.start_value': 3.0, 'output.value': 2.999550020249566, 'log': '', 'Generator.py': ''}, {'clock_tick': 4.0, 'input.start_value': 4.0, 'output.value': 3.998933418663416, 'log': '', 'Generator.py': ''}, {'clock_tick': 5.0, 'input.start_value': 5.0, 'output.value': 4.997916927067833, 'log': '', 'Generator.py': ''}, {'clock_tick': 6.0, 'input.start_value': 6.0, 'output.value': 5.996400647944459, 'log': '', 'Generator.py': ''}, {'clock_tick': 7.0, 'input.start_value': 7.0, 'output.value': 6.994284733753277, 'log': '', 'Generator.py': ''}, {'clock_tick': 8.0, 'input.start_value': 8.0, 'output.value': 7.991469396917269, 'log': '', 'Generator.py': ''}, {'clock_tick': 9.0, 'input.start_value': 9.0, 'output.value': 8.987854919801103, 'log': '', 'Generator.py': ''}, {'clock_tick': 10.0, 'input.start_value': 10.0, 'output.value': 9.983341664682815, 'log': '', 'Generator.py': ''}, {'clock_tick': 11.0, 'input.start_value': 11.0, 'output.value': 10.977830083717482, 'log': '', 'Generator.py': ''}, {'clock_tick': 12.0, 'input.start_value': 12.0, 'output.value': 11.971220728891936, 'log': '', 'Generator.py': ''}, {'clock_tick': 13.0, 'input.start_value': 13.0, 'output.value': 12.963414261969486, 'log': '', 'Generator.py': ''}, {'clock_tick': 14.0, 'input.start_value': 14.0, 'output.value': 13.954311464423649, 'log': '', 'Generator.py': ''}, {'clock_tick': 15.0, 'input.start_value': 15.0, 'output.value': 14.943813247359921, 'log': '', 'Generator.py': ''}]
if __name__ == "__main__":
    create_node().csv.run_test_with_validation_data(verif_dict=testdata)




