import inspect
import logging
import MavicMaxGui
import _thread
import NodeCore.runner
import NodeCore.runner2
import NodeCore
from app.gui.api import Api
log=logging.getLogger(__file__)

import os
import pathlib
from fnmatch import fnmatch
from pathlib import Path
from config import settings


def list_all_nodes(node_path: Path):
    nodes=[]
    for path, subdirs, files in os.walk(node_path):
        for name in files:
            if fnmatch(name, "[!_]*.py"):
                p = pathlib.PurePath(path, name).as_posix()
                p=p.replace(node_path.as_posix(), '')
                p=p.replace('.py', '')
                nodes.append(p)
    list.sort(nodes)
    return nodes


def show_start_node_gui(nodepath:str):
    def start_callback(nodepath: str, user_input: dict):
        MavicMaxGui.Dialog.close()
        NodeCore.runner2.NodeRunner.start_node(nodepath, user_input)

    module = NodeCore.runner2.NodeRunner.import_node(nodepath)
    signature = inspect.signature(module.create_node)
    log.info(f"{signature=}")
    elements = {}
    for i in signature.parameters.values():
        name: str = i.name
        if name not in ['plugin_name', 'parent']:
            if isinstance(i.default, list):
                default = i.default
            else:
                # default=str(i.default)
                default = i.default
            elements.update({name: default})
    print(f'{elements=}')
    MavicMaxGui.Dialog.Start.show(title=nodepath,
                                  args=elements,
                                  predefined_args={},
                                  start_callback=lambda user_input, nodepath=nodepath: start_callback(nodepath, user_input),
                                  view_callback=lambda nodepath: MavicMaxGui.Dialog.Popup.show(title=nodepath, message="VIEW", level=2),
                                  code_callback=lambda nodepath: MavicMaxGui.Dialog.Popup.show(title=nodepath, message=NodeCore.runner2.NodeRunner.get_node_code(nodepath=nodepath).read_text(), level=2),
                                  help_callback=lambda nodepath: MavicMaxGui.Dialog.Popup.show(title=nodepath, message=NodeCore.runner2.NodeRunner.get_node_help(nodepath=nodepath), level=2),
                                  kill_callback = lambda nodepath: NodeCore.runner2.NodeRunner.kill_node(nodepath=nodepath))

def run(port: int = 8079):
    def create_node_menu(menu_name:str = '/start'):
        MavicMaxGui.menu.add_menu_item('/devel/logs/a', lambda x: print("din mamma"))
        for node in list_all_nodes(settings.filesystem.node_dir):
            menu_path = menu_name + node
            MavicMaxGui.menu.add_menu_item(menu_path, lambda x, node=node: show_start_node_gui(node))


    _thread.start_new_thread( create_node_menu, () )
    _thread.start_new_thread(MavicMaxGui.start_www, (port, ))
    NodeCore.node_created_callback = node_created_callback
    NodeCore.node_deleted_callback = node_deleted_callback


def node_created_callback(node_name_path):
    MavicMaxGui.menu.add_menu_item(f'/running/{node_name_path}', callback=lambda x:NodeCore.runner2.NodeRunner.show_view(nodepath=node_name_path))

def node_deleted_callback(node_name_path):
    MavicMaxGui.menu.rm_menu_item(f'/running/{node_name_path}')

if __name__ == "__main__":
    run()


