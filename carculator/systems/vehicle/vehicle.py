from cosapp.base import System

from carculator.systems.powertrain import Powertrain
from carculator.systems.vehicle import VehicleSpecs


class VehicleModel(System):
    def setup(
        self,
        vehicle_size=None,
        cycle_name=None,
    ):
        self.add_child(
            Powertrain("powertrain"),
            pulling={"type": "powertrain_type", "mass": "powertrain_mass"},
        )
        
        self.add_child(
            VehicleSpecs(
                "vehicle_specs", vehicle_size=vehicle_size, cycle_name=cycle_name
            ),
            pulling=["curb_mass", "vehicle_size", "cycle_name"],
        )