from cosapp.base import System
from scipy.constants import g


class VehicleModel(System):
    def setup(self):
        self.add_inward("engine_efficiency", unit="")
        self.add_inward("transmission_efficiency", unit="")
        self.add_inward("fuel_cell_system_efficiency", unit="")
        self.add_inward("driving_mass", unit="kg")
        self.add_inward("rolling_resistance_coeff", unit="")
        self.add_inward("velocity", unit="m/s")
        self.add_inward("")

        self.add_outward("motive_energy", "Wh")
        self.add_outward("recuperated_energy")
