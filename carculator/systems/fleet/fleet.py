from cosapp.base import System
from typing import Union, List
import numpy as np

from carculator.systems.vehicle import VehicleModel


class Fleet(System):
    def setup(
        self,
        sizes: Union[None, List[str], str] = "Small",
        cycle: Union[None, str, np.ndarray] = "WLTC",
        powertrains: Union[None, List[str], str] = "BEV",
    ):
        if isinstance(sizes, str):
            sizes = [sizes]
        if isinstance(powertrains, str):
            powertrains = [powertrains]

        for i, size in enumerate(sizes):
            for j, powertrain in enumerate(powertrains):
                self.add_child(
                    VehicleModel(
                        f"vec_{int(i*len(powertrains)+j)}",
                        vehicle_size=size,
                        cycle_name=cycle,
                        powertrain=powertrain,
                    )
                )
