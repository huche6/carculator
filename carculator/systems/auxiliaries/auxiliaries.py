from cosapp.base import System
from carculator.ports import Mass


class Auxiliaries(System):
    def setup(self):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_inward("heating_thermal_demand", 1.0)
        self.add_inward("heating_energy_consumption", 1.0)
        self.add_inward("cooling_thermal_demand", 1.0)
        self.add_inward("cooling_energy_consumption", 1.0)
        self.add_inward("power_base_demand")
        self.add_inward("electric_onboard_mass", unit="kg")

        self.add_outward("auxiliary_power_demand", 1.0)

    def compute(self):
        self.auxiliary_power_demand = (
            self.power_base_demand
            + self.heating_thermal_demand * self.heating_energy_consumption
            + self.cooling_thermal_demand * self.cooling_energy_consumption
        )

        self.mass_out.mass = self.mass_in.mass + self.electric_onboard_mass
