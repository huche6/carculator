from cosapp.base import System


class FuelTank(System):
    def setup(self, mass, cost):
        self.add_inward("mass", None, desc="mass of the fuel tank")
        self.add_inward("cost", None, desc="cost of the fuel tank")
