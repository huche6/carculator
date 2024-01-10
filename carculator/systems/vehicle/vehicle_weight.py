from cosapp.base import System


class VehicleWeight(System):
    def setup(self):
        self.add_inward("cargo_mass", unit="kg")
        self.add_inward("average_passengers", 1.5, unit="")
        self.add_inward("average_passengers_mass", 70, unit="kg")
        self.add_inward("curb_mass", unit="kg")

        self.add_outward("total_cargo_mass", unit="kg")
        self.add_outward("driving_mass", unit="kg")

    def compute(self):
        self.total_cargo_mass = (
            self.cargo_mass + self.average_passengers * self.average_passengers_mass
        )
        self.driving_mass = self.curb_mass + self.total_cargo_mass
