import dataclasses
import importlib
import logging
import threading
import time
import traceback
from abc import ABC
from pathlib import Path

import MavicMaxGui
import NodeCore
from NodeCore import Node
from config import settings
log = logging.getLogger(__name__)

message_field_name: str = 'message_screen'


@dataclasses.dataclass
class _NodeRunner():
    node_list: [Node] = dataclasses.field(default_factory=list)
    loop_delay_ms: int = 100
    loop_nbr:int  = 0
    running:bool = False

    def import_node(self, nodepath):
        node_path_abs = settings.filesystem.node_module_loc + nodepath.replace('/', '.')
        module = importlib.import_module(node_path_abs)
        return module

    def get_node_code(self, nodepath: str) -> Path:
        absolute_path = settings.filesystem.node_dir.absolute()
        absolute_path = absolute_path.joinpath(Path(nodepath[1:] + '.py'))
        return absolute_path

    def get_node_help(self, nodepath: str) -> str:
        node_module = self.import_node(nodepath)
        return str(node_module.create_node.__doc__)

    def filter_dict(self, d:dict, startswith:str='_') -> dict:
        return dict(filter(lambda elem: not elem[0].startswith(startswith), d.items()))


    def start_node(self, nodepath: str, user_input: dict):
        node_module = self.import_node(nodepath)
        node = node_module.create_node(parent=None, **user_input)

        #input_dict: dict = self.filter_dict(node.input.__dict__)
        #output_dict: dict = self.filter_dict(node.output.__dict__)
        input_dict: dict = node.input.__dict__
        output_dict: dict = node.output.__dict__

        if message_field_name in output_dict:
            del output_dict[message_field_name]
        view = MavicMaxGui.View(gui_items_input=input_dict, gui_items_output=output_dict)
        MavicMaxGui.MyApp.show_view(view)
        self.node_list.append((node, nodepath, view))
        NodeCore.runner2.NodeRunner.start_execution_in_background()
        MavicMaxGui.menu.add_menu_item(f'/running/{node.node_name_path}',
                                       callback=lambda x: self.show_view(nodepath))

    def show_view(self, nodepath:str):
        for node, _nodepath, view in self.node_list:
            if nodepath==_nodepath:
                MavicMaxGui.MyApp.show_view(view)

    def kill_node(self, nodepath:str):
        log.info("killing", nodepath)
        for node, _nodepath, view in self.node_list:
            if nodepath==_nodepath:
                log.info("killing", _nodepath, node, self.node_list)
                self.node_list.remove((node, _nodepath, view))
                log.info(self.node_list)
                MavicMaxGui.menu.rm_menu_item(f'/running/{node.node_name_path}')



    def execute_node_list(self):
        #log.info(f"loop:{Node.clock_tick}")
        for node, nodepath, view in self.node_list:
            try:
                node.run_in_threads=True
                node.execute_node()
                input_dict: dict = self.filter_dict(node.input.__dict__)
                output_dict: dict = self.filter_dict(node.output.__dict__)
                if message_field_name in output_dict:
                    if node.output.message_screen != "":
                        view.update_info_field(output_dict[message_field_name]+'\n')
                        node.output.message_screen = ""
                    del output_dict[message_field_name]

                view.update_input_fields(input_dict)
                view.update_output_fields(output_dict)
                node.update_input_fields_from_dict(view.get_changed_fields())
            except:
                MavicMaxGui.Dialog.Popup.show(title="Error", message=traceback.format_exc())
                log.exception("qq11")
                time.sleep(20)

        Node.clock_tick = Node.clock_tick +1

    def loop(self):
        while self.running:
            self.execute_node_list()
            time.sleep(self.loop_delay_ms/1000)

    def stop(self):
        self.running=False

    def start_execution_in_background(self):
        t = threading.Thread(target=self.loop)
        self.running=True
        t.start()

NodeRunner=_NodeRunner()

if __name__ == "__main__":
    import test_nodes.nodes.Generator
    node = test_nodes.nodes.Generator.create_node()

    NodeRunner.start_node(node)
    NodeRunner.start_execution_in_background()
    time.sleep(4)
    NodeRunner.stop()
    log.info("stop")
    time.sleep(2)

