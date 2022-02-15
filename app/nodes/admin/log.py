import copy
import time
import traceback
from dataclasses import dataclass, field
from datetime import datetime
from pathlib import Path

import DroneSdk
import MavicMaxGui
import NodeCore
from NodeCore import Node, Event, plugin_name
import DroneSdk
Sdk=DroneSdk.get_drone_sdk()

def create_node(plugin_name=plugin_name(__file__), parent=None, autopull:bool=False):
    '''
        Git functions
    '''
    return Git(plugin_name=plugin_name, parent=parent, autopull=autopull)

@dataclass
class Input:
    clear: Event = field(default_factory=Event)
    upd_logcat: Event = field(default_factory=Event)
    upd_log: Event = field(default_factory=Event)
    grep: str = ""
    exclude: str = "_message("
    lines: int = 250
    time_in: str = ''
@dataclass
class Output:
    time: str = ''
    message_screen: str = ''
    lines_ut: int = 250

class Git(Node):
    input: Input
    output: Output
    def __init__(self, autopull: bool=True, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)
        self.input.clear.register(lambda : Sdk.Admin.restart_app())
        self.input.upd_logcat.register(lambda : self.refresh('logcat.txt'))
        self.input.upd_log.register(lambda : self.refresh('mavicmax2.log'))

    def get_log(self, logfile_abs: str, grep:str="", exclude:str="", nbr_of_lines=20):
        lines = Path(logfile_abs).read_text().split('\n')
        grepped_lines=[]
        reversed_lines = lines[::-1]
        index:int=0
        for line in reversed_lines:
            if index>nbr_of_lines: break
            if grep in line and exclude!='' and not exclude in line:
                grepped_lines.append(line)
                index+=1
        return "\n".join(grepped_lines)

    def refresh(self, filename):
        logfile_abs = Sdk.Admin.get_log_dir()+f'/{filename}'
        header = f"From file:{logfile_abs}\n"
        self.output.message_screen = "CLR" +  header + self.get_log(logfile_abs, self.input.grep,  self.input.exclude, self.input.lines)

    def run(self) -> None:
        today = datetime.now()
        self.output.time = today.strftime("%H:%M:%S.%f")[:-5]
        self.input.time_in = self.output.time
        self.output.lines_ut = self.input.lines
        pass

if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

