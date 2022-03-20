import copy
import logging
import time
import traceback
from dataclasses import dataclass, field
import NodeCore
from NodeCore import Node, Event, plugin_name
import DroneSdk.sdk as sdk



def create_node(plugin_name=plugin_name(__file__), parent=None, autopull:bool=False):
    '''
        Git functions
    '''
    return Git(plugin_name=plugin_name, parent=parent, autopull=autopull)

@dataclass
class Input:
    restart: Event = field(default_factory=Event)
    pull: Event = field(default_factory=Event)
    status: Event = field(default_factory=Event)
    select: str = ""
    autopull: bool = False
@dataclass
class Output:
    dir: str = ''
    branch: str = ''
    message_screen: str = ''

class Git(Node):
    input: Input
    output: Output
    def __init__(self, autopull: bool=False, *args, **kwargs) -> None:
        input, output = Input(), Output()
        super().__init__(input=input, output=output, *args, **kwargs)
        self.input.restart.register(lambda : sdk.restart())
        self.input.pull.register(lambda : self.pull())
        self.input.status.register(lambda : self.status())
        self.input.autopull = autopull
        self.output.dir = sdk.get_app_root()+'/git/mavicmax2'
        self.input.select = {'a':'=a', 'b':'=b'}


    def pull(self):
        try:
            self.output.message_screen = sdk.git_pull(self.output.dir)
            if "Already-up-to-date" not in self.output.message_screen:
                pass
                #sdk.restart()
            #self.output.branch = branch.split('/')[-1]
        except:
            self.output.branch = "Error1"
            print(f"ERROR{traceback.format_exc()}")
            logging.exception("")


    def status(self):
        self.output.message_screen = sdk.git_status(self.output.dir)

    def run(self) -> None:
        if self.input.autopull:
            self.pull()
            time.sleep(2)

if __name__ == "__main__":
    NodeCore.run_from_main(__file__)

