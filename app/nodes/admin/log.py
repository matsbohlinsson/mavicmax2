from dataclasses import dataclass, field
from datetime import datetime
import NodeCore
from NodeCore import Node, Event, plugin_name
import DroneSdk
import DroneSdk.sdk as sdk
from app.util import grep_log


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
        self.input.clear.register(lambda : sdk.restart())
        self.input.upd_logcat.register(lambda : self.refresh('logcat.txt'))
        self.input.upd_log.register(lambda : self.refresh('mavicmax2.log'))


    def refresh(self, filename):
        DroneSdk.sdk.get_log_dir()
        logfile_abs = sdk.get_log_dir()+f'/{filename}'
        header = f"From file:{logfile_abs}\n"
        self.output.message_screen = "CLR" +  header + grep_log(logfile_abs, self.input.grep,  self.input.exclude, self.input.lines)

    def run(self) -> None:
        today = datetime.now()
        self.output.time = today.strftime("%H:%M:%S.%f")[:-5]
        self.input.time_in = self.output.time
        self.output.lines_ut = self.input.lines
        pass

if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

