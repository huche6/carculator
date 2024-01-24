import numpy as np
import xarray as xr
from cosapp.base import System

from carculator.ports import Mass
from carculator.systems.powertrain.electrical import ElectricalPowertrain
from carculator.systems.powertrain.powertrain_specs import PowertrainSpecs
from carculator.systems.powertrain.thermal import ThermalPowertrain


class Powertrain(System):
    def setup(self, type):
        self.add_input(Mass, "mass_in")
        self.add_output(Mass, "mass_out")

        self.add_child(
            PowertrainSpecs("powertrain_specs", type=type),
            pulling=["type", "curb_mass"],
        )

        self.connect(self.powertrain_specs.mass_in, self.mass_in)

        if type in ["ICEV-p", "ICEV-d", "ICEV-g", "HEV-p", "HEV-d", "PHEV-p", "PHEV-d"]:
            self.add_child(ThermalPowertrain("thermal_powertrain"))
            self.connect(
                self.thermal_powertrain.inwards, self.powertrain_specs.outwards, "power"
            )
            # self.connect(
            #    self.thermal_powertrain.mass_in, self.powertrain_specs.mass_out
            # )
            # self.connect(self.mass_out, self.thermal_powertrain.mass_out)

        if type in ["HEV-p", "HEV-d", "BEV", "FCEV"]:
            self.add_child(
                ElectricalPowertrain("electrical_powertrain"),
                pulling=["speed", "motive_energy", "engine_efficiency"],
            )
            self.connect(
                self.electrical_powertrain.inwards,
                self.powertrain_specs.outwards,
                "power",
            )
            # self.connect(
            #    self.electrical_powertrain.mass_in, self.powertrain_specs.mass_out
            # )

        if len(self.children) > 2:
            self.connect(
                self.thermal_powertrain.mass_in, self.powertrain_specs.mass_out
            )
            self.connect(
                self.electrical_powertrain.mass_in, self.thermal_powertrain.mass_out
            )
            self.connect(self.mass_out, self.electrical_powertrain.mass_out)
        else:
            child = list(self.children).pop(1)
            self.connect(self[child].mass_in, self.powertrain_specs.mass_out)
            self.connect(self.mass_out, self[child].mass_out)

        # self.connect(self.mass_out, self.electrical_powertrain.mass_out)
