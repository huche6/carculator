from cosapp.base import System
import numpy as np
from carculator_utils import (
    get_standard_driving_cycle_and_gradient,
    get_efficiency_coefficients,
)


class EngineSpecs(System):
    def setup(self, cycle_name=None, vehicle_type=None, vehicle_size=None):
        self.add_inward("cycle_name", cycle_name, dtype=(str, np.ndarray))
        self.add_inward("vehicle_type", vehicle_type, dtype=str)
        self.add_inward("vehicle_size", vehicle_size, dtype=list)

        self.add_outward("cycle", None, dtype=np.ndarray)
        self.add_outward("gradient", None, dtype=(str, np.ndarray))
        self.add_outward("efficiency_coefficients", None, dtype=dict)

    @classmethod
    def cycle_and_gradient(cls, name, vehicle_type, vehicle_size, cycle_name):
        s = cls(name)

        for var_name, var in zip(
            ["vehicle_type", "vehicle_size", "cycle_name"],
            [vehicle_type, vehicle_size, cycle_name],
        ):
            s[var_name] = var

        s.cycle, s.gradient = get_standard_driving_cycle_and_gradient(
            vehicle_type, vehicle_size, cycle_name
        )

        assert len(s.cycle) == len(
            s.gradient
        ), "The length of the driving cycle and the gradient must be the same."

        s.efficiency_coefficients = get_efficiency_coefficients(vehicle_type)

        return s
