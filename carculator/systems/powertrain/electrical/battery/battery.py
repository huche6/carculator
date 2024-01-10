from cosapp.base import System
from carculator.ports import Mass
import numpy as np
from carculator_utils import replace_values_in_array


class Battery(System):
    def setup(self):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_inward("engine_power")
        self.add_inward("cell_power_density")
        self.add_inward("combustion_power_share")
        self.add_inward("cell_mass_share")

        self.add_outward("power")
        self.add_outward("cell_mass", unit="kg")
        self.add_outward("bop_mass", unit="kg")

    def compute(self):
        combustion_power_share = (
            self.combustion_power_share if self.combustion_power_share > 0 else 1
        )
        self.power = self.engine_power * (combustion_power_share)
        self.cell_mass = (
            self.power
            / replace_values_in_array(self.cell_power_density, lambda x: x == 0)
            * combustion_power_share
        )

        self.bop_mass = (
            self.cell_mass * (1 - self.cell_mass_share) * (combustion_power_share)
        )

        self.mass_out.mass = self.mass_in.mass + self.cell_mass + self.bop_mass
