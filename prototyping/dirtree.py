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
                p.replace(node_path.as_posix(), '')
                p.replace('.py', '')
                nodes.append(p.replace(node_path.as_posix(),''))
    return nodes



node_list = list_all_nodes(settings.filesystem.node_dir)
print(node_list)
