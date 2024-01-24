from cosapp.base import System
from carculator.systems.powertrain.electrical.engine import ElectricEngine
from carculator.systems.powertrain.electrical.battery import Battery
from carculator.systems.powertrain.electrical.converter import Converter
from carculator.systems.powertrain.electrical.inverter import Inverter
from carculator.ports import Mass


class ElectricalPowertrain(System):
    def setup(self):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_child(
            ElectricEngine("electric_engine"),
            pulling={
                "power": "power",
                "combustion_power_share": "combustion_power_share",
                "speed": "speed",
                "motive_energy": "motive_energy",
                "efficiency": "engine_efficiency",
            },
        )
        self.add_child(Battery("battery"), pulling=["combustion_power_share"])
        self.add_child(Converter("converter"), pulling={"mass": "converter_mass"})
        self.add_child(Inverter("inverter"), pulling={"mass": "inverter_mass"})

        self.connect(
            self.battery.inwards,
            self.electric_engine.outwards,
            "engine_power",
        )

        self.connect(self.electric_engine.mass_in, self.mass_in)
        self.connect(self.battery.mass_in, self.electric_engine.mass_out)
        self.connect(self.converter.mass_in, self.battery.mass_out)
        self.connect(self.inverter.mass_in, self.converter.mass_out)
        self.connect(self.mass_out, self.inverter.mass_out)
