from cosapp.base import System
from carculator.ports import Mass


class Tank(System):
    def setup(self):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_inward("fuel_mass", unit="kg")
        self.add_inward("tank_mass", unit="kg")

    def compute(self):
        self.mass_out.mass = self.mass_in.mass + self.fuel_mass + self.tank_mass
