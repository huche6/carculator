from cosapp.base import System


class Auxiliaries(System):
    def setup(self):
        self.add_inward("heating_thermal_demand", 1.0)
        self.add_inward("heating_energy_consumption", 1.0)
        self.add_inward("cooling_thermal_demand", 1.0)
        self.add_inward("cooling_energy_consumption", 1.0)

        self.add_outward("auxiliary_power_demand", 1.0)

    def compute(self):
        self.auxiliary_power_demand = (
            self.heating_thermal_demand * self.heating_energy_consumption
            + self.cooling_thermal_demand * self.cooling_energy_consumption
        )
