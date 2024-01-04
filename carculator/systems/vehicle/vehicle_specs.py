from cosapp.base import System
import numpy as np
from carculator_utils.driving_cycles import (
    detect_vehicle_type,
    get_default_driving_cycle_name,
)


class VehicleSpecs(System):
    def setup(
        self,
        vehicle_size=None,
        cycle_name=None,
    ):
        self.add_inward("vehicle_type", detect_vehicle_type(vehicle_size))
        self.add_inward("vehicle_size", vehicle_size)
        self.add_inward(
            "cycle_name",
            cycle_name
            if type(cycle_name) in [np.ndarray, str, list]
            else get_default_driving_cycle_name(self.vehicle_type),
        )

        self.add_outward(
            "curb_mass", None, desc="Mass of the vehicle without passenger and cargo."
        )
        
