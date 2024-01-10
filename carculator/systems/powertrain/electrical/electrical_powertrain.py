from cosapp.base import System
from carculator.systems.powertrain.electrical.engine import ElectricEngine
from carculator.systems.powertrain.electrical.battery import Battery
from carculator.ports import Mass


class ElectricalPowertrain(System):
    def setup(self):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_child(
            ElectricEngine("electric_engine"),
            pulling=["power", "combustion_power_share"],
        )
        self.add_child(Battery("battery"), pulling=["combustion_power_share"])

        self.connect(
            self.battery.inwards,
            self.electric_engine.outwards,
            "engine_power",
        )

        self.connect(self.electric_engine.mass_in, self.mass_in)
        self.connect(self.battery.mass_in, self.electric_engine.mass_out)
        self.connect(self.mass_out, self.battery.mass_out)
