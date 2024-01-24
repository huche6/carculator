from cosapp.base import System
from carculator.ports import Mass


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

        self.add_outward("ttw_efficiency")

    def compute(self):
        return
