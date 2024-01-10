from cosapp.base import System

import xarray as xr
from carculator.systems.powertrain import Powertrain
from carculator.systems.glider import Glider
from carculator.systems.auxiliaries import Auxiliaries
from carculator.systems.vehicle.vehicle_weight import VehicleWeight
from carculator.systems.vehicle.vehicle_dynamic import Dynamics
from carculator.ports import Mass


class VehicleModel(System):
    def setup(self, vehicle_size=None, cycle_name=None, powertrain=None):
        self.add_child(
            Glider("glider", vehicle_size=vehicle_size, cycle_name=cycle_name),
            pulling={"glider_size": "size", "cycle_name": "cycle_name"},
        )
        self.add_child(
            VehicleWeight("vehicle_weight"),
            pulling=["curb_mass", "total_cargo_mass", "driving_mass"],
        )
        self.add_child(Dynamics("vehicle_dynamic"))
        # self.add_child(VehicleEnergy("vehicle_power"))
        self.add_child(
            Powertrain("powertrain", type=powertrain), pulling=["mass_out", "curb_mass"]
        )
        self.add_child(Auxiliaries("auxiliaries"))

        self.connect(self.glider.mass_out, self.powertrain.mass_in)

        self.connect(
            self.vehicle_dynamic.inwards, self.vehicle_weight.outwards, "driving_mass"
        )

        # design method
        # design = self.add_design_method("scale_mass")
        self.add_unknown("curb_mass")
        self.add_equation("mass_out.mass - curb_mass == 0")
