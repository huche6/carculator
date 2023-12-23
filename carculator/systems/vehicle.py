from cosapp.base import System
import numpy as np
import xarray as xr
from typing import Union


class VehicleModel(System):
    def setup(
        self, array: xr.DataArray = None, cycle: Union[None, str, np.ndarray] = None
    ):
        self.add_property(
            "array",
            array,
        )
        self.add_inward("country", None, dtype=str, desc="country code")
        self.add_inward(
            "cycle",
            cycle,
            dtype=(str, np.ndarray),
            desc="name of a driving cycle, or custom driving cycle.",
        )
        self.add_inward(
            "gradient",
            None,
            dtype=np.ndarray,
            desc="series of gradients, for each second of the driving cycle",
        )
        self.add_inward(
            "energy_storage",
            None,
            dtype=dict,
            desc="dictionary with selection of battery chemistry, capacity and origin for each powertrain-size-year combination",
        )
        self.add_inward(
            "electric_utility_factor",
            None,
            dtype=float,
            desc="fraction of electricity that is generated from renewable sources",
        )
        self.add_inward(
            "drop_hybrids",
            True,
            dtype=bool,
            desc="boolean, if True, hybrid vehicles are dropped from the inventory",
        )
        self.add_inward(
            "payload",
            None,
            desc="dictionary with payload for each powertrain-size-year combination",
        )
        self.add_inward("annual_mileage", None)
        self.add_inward(
            "energy_target", None, desc="dictionary with energy target for each year"
        )
        self.add_inward(
            "energy_consumption",
            None,
            dtype=dict,
            desc="dictionary with energy consumption for each powertrain-size-year combination",
        )
        self.add_inward("engine_efficiency", None, dtype=dict)
        self.add_inward("transmission_efficiency", None, dtype=dict)
        self.add_inward(
            "target_range",
            None,
            dtype=dict,
            desc="dictionary with target range for each powertrain-size-year combination",
        )
        self.add_inward("target_mass", None, dtype=dict)
        self.add_inward("power", None, dtype=dict)
        self.add_inward("fuel_blend", None, dtype=dict)
        self.add_inward("ambiant_temperature", None, dtype=float)
        self.add_inward("indoor_temperature", 20.0, dtype=float)

    @property
    def array(self):
        return self._array

    @array.setter
    def array(self, dict_array):
        self._array = xr.DataArray.from_dict(dict_array)
