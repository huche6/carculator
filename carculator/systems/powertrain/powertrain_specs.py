from cosapp.base import System
from carculator.ports import Mass
import numpy as np
import xarray as xr


class PowertrainSpecs(System):
    def setup(self, type):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_inward("type", type, dtype=(list, str, np.ndarray))

        self.add_inward("power_to_mass_ratio", 1.0)
        self.add_inward("curb_mass", 1.0, unit="kg")
        self.add_inward("powertrain_mass_per_power", 1.0)
        self.add_inward("powertrain_fixed_mass", 1.0)

        self.add_outward(
            "power",
            1.0,
        )
        self.add_outward("mass", 1.0, dtype=(float, np.ndarray, xr.DataArray))

    def compute(self):
        self.power = self.power_to_mass_ratio * self.curb_mass * 1e-3
        self.mass = (
            self.power * self.powertrain_mass_per_power + self.powertrain_fixed_mass
        )

        self.mass_out.mass = self.mass_in.mass + self.mass
