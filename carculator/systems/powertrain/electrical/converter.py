from cosapp.base import System
from carculator.ports import Mass


class Converter(System):
    def setup(self):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_inward("mass", unit="kg")

    def compute(self):
        self.mass_out.mass = self.mass + self.mass_in.mass
