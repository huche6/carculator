from cosapp.base import System
import numpy as np

from carculator.ports import Mass

from carculator_utils.driving_cycles import (
    detect_vehicle_type,
    get_default_driving_cycle_name,
)


class Glider(System):
    def setup(
        self,
        vehicle_size=None,
        cycle_name=None,
    ):
        self.add_output(Mass, "mass_out")

        self.add_inward("vehicle_type", detect_vehicle_type(vehicle_size))
        self.add_inward("glider_size", vehicle_size)
        self.add_inward(
            "cycle_name",
            cycle_name
            if type(cycle_name) in [np.ndarray, str, list]
            else get_default_driving_cycle_name(self.vehicle_type),
        )

        self.add_inward("mass", 1.0, dtype=float)
        self.add_inward("lightweighting", 0.0, unit="")

    def compute(self):
        self.mass_out.mass = self.mass * (1 - self.lightweighting)
