from cosapp.base import System
import numpy as np
import xarray as xr
from typing import Union
from carculator.systems.vehicle.vehicle_specs import VehicleSpecs
from carculator_utils.driving_cycles import detect_vehicle_type


class VehicleModel(System):
    def setup(
        self,
        array: xr.DataArray = None,
        cycle_name=None,
    ):
        self.add_inward(
            "vehicle_type", detect_vehicle_type(list(array.coords["size"].values))
        )
        self.add_inward("vehicle_size", list(array.coords["size"].values))
        self.add_inward("cycle_name", cycle_name)

        self.add_child(
            VehicleSpecs("vehicle_specs").cycle_and_gradient(
                "vehicle_specs", self.vehicle_type, self.vehicle_size, cycle_name
            ),
            pulling=["vehicle_type", "vehicle_size", "cycle"],
        )
