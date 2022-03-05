from __future__ import annotations
import logging
from dataclasses import dataclass, field
from NodeCore import Event, General, plugin_name
import app.util
import app.nodes.drone.flightcontroller

class CameraFollow(General):
    input: Input
    output: Output

@dataclass
class Input:
    ac_lat: float = 58
    ac_lon: float = 11
    ac_altitude: float = 10
    ac_yaw: float = 180

    tr_lat: float = 58.00001
    tr_lon: float = 11.00001
    tr_altitude: float = 0
    tr_course: float = 100

@dataclass
class Output:
    attitude: float = 0
    yaw: float = 0
    distance: float = 10


def init(input: Input, output: Output, log: logging.Logger) -> None:
    pass

def main_loop(input: Input, output: Output, log: logging.Logger) -> None:
    ac_loc = app.util.Location(input.ac_lat, input.ac_lon, input.ac_altitude)
    tr_loc = app.util.Location(input.tr_lat, input.tr_lon, input.tr_altitude)
    output.distance= ac_loc.distance_to(tr_loc)
    output.yaw = app.util.Course.diff(desired=ac_loc.course_to(tr_loc), measured=input.ac_yaw)
    output.attitude = ac_loc.incline_to(tr_loc)



def create_node(plugin_name=plugin_name(__file__), parent=None, yaw:float=0, pitch:float=-90, mode={'a':'=a', 'b':'=b', 'c':'=c'}) -> CameraFollow:
    '''
    Camera follow
    :param plugin_name:
    :param parent:
    :param yaw:
    :param pitch:
    :return:
    '''
    self = CameraFollow(plugin_name=plugin_name, init=init, run=main_loop, run_post=None, parent=parent, input=Input(),output=Output())
    return self


if __name__ == "__main__":
    import NodeCore
    from pathlib import Path
    NodeCore.run_from_main(__file__, import_base='app.nodes.devel.followme.', csv_dir_path=Path('../../csv_testdata'))
