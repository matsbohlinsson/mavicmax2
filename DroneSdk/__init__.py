import dataclasses
import logging
import math

import DroneSdk.AndroidBindings
import DroneSdk.DroneDji
import DroneSdk.DroneSimulator as sim


log = logging.getLogger(__file__)

def get_drone_sdk() -> DroneDji.Sdk:
    import app.util
    if app.util.platform.is_running_on_android():
        return DroneSdk.DroneDji.Sdk
    else:
        return sim.Sdk
