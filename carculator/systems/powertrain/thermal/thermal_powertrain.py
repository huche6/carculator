from cosapp.base import System
from carculator.systems.powertrain.thermal.engine import ThermalEngine
from carculator.systems.powertrain.thermal.tank import Tank
from carculator.ports import Mass


class ThermalPowertrain(System):
    def setup(self):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_child(
            ThermalEngine("thermal_engine"),
            pulling=["power", "combustion_power_share"],
        )
        self.add_child(Tank("tank"))

        self.connect(self.thermal_engine.mass_in, self.mass_in)
        self.connect(self.tank.mass_in, self.thermal_engine.mass_out)
        self.connect(self.mass_out, self.tank.mass_out)
