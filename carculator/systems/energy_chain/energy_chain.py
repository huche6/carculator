from cosapp.base import System
from carculator.ports import Mass
import numpy as np


class EnergyDistribution(System):
    def setup(self):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_inward("mass", unit="kg", desc="Mass of the energy distribution unit")

    def compute(self):
        self.mass_out.mass = self.mass_in.mass + self.mass


class Transmission(System):
    def setup(self):
        self.add_inward("fuel_cell_system_efficiency")
        self.add_inward("transmission_efficiency")
        self.add_inward("engine_efficiency")
        self.add_inward("engine_load")
        self.add_inward("dict_efficiencies", {0.0: 0.0, 1.0: 1.0}, dtype=dict)

        self.add_outward("ttw_efficiency")
        self.add_outward("efficiency", unit="")

    def compute(self):
        self.efficiency = np.interp(
            self.engine_load,
            np.array(list(self.dict_efficiencies.keys())),
            np.array(list(self.dict_efficiencies.values())),
        )
