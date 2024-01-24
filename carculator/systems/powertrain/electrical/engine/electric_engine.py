from cosapp.base import System
from carculator.ports import Mass
import numpy as np


class ElectricEngine(System):
    def setup(self):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_inward("electric_mass_per_power", 1.0)
        self.add_inward("electric_fixed_mass", 1.0)
        self.add_inward("combustion_power_share")
        self.add_inward("speed", 50.0, unit="m/s")
        self.add_inward("engine_load", 1.0)
        self.add_inward("motive_energy", 1.0)
        self.add_inward("dict_efficiencies", {0.0: 0.0, 1.0: 1.0}, dtype=dict)

        self.add_inward("power", 1.0)

        self.add_outward("mass", 1.0)
        self.add_outward("engine_power")
        self.add_outward("efficiency")

        self.add_unknown("engine_load")
        self.add_equation(
            "speed - engine_load*engine_power/motive_energy == engine_load"
        )

    def compute(self):
        # Mass
        self.mass = self.power * self.electric_mass_per_power + self.electric_fixed_mass
        self.mass_out.mass = self.mass_in.mass + self.mass

        # Power
        self.engine_power = self.power * (
            1 - np.clip(self.combustion_power_share, a_min=0, a_max=1)
        )

        self.efficiency = np.interp(
            self.engine_load,
            np.array(list(self.dict_efficiencies.keys())),
            np.array(list(self.dict_efficiencies.values())),
        )
