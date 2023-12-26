from cosapp.base import System
import xarray as xr
from carculator_utils.driving_cycles import (
    detect_vehicle_type,
    get_standard_driving_cycle_and_gradient,
)
import numpy as np
import inspect


from cosapp.base import System
import xarray as xr
from carculator_utils.driving_cycles import (
    detect_vehicle_type,
    get_standard_driving_cycle_and_gradient,
)
import numpy as np
import inspect


class VehicleSpecs(System):
    def setup(self):
        # Specs
        self.add_inward("cycle_name", None, dtype=(str, np.ndarray))
        self.add_inward(
            "vehicle_type",
            None,
            dtype=str,
        )
        self.add_inward("vehicle_size", None, dtype=(str, list))

        # Mass properties
        self.add_inward("glider_base_mass", None, dtype=xr.DataArray)
        self.add_inward("lightweighting", None, dtype=xr.DataArray)

        # Not sure that should be here: used to compute velocity and acceleration
        self.add_inward("cycle", None, dtype=np.ndarray)
        self.add_inward("gradient", None, dtype=(str, np.ndarray))

        self.add_outward(
            "curb_mass", None, dtype=xr.DataArray, desc="mass of the vehicle and fuel"
        )
        self.add_outward(
            "cargo_mass",
            None,
            dtype=xr.DataArray,
            desc="mass of the cargo and passengers",
        )
        self.add_outward(
            "driving_mass", None, dtype=xr.DataArray, desc="curb_mass + cargo_mass"
        )

    @classmethod
    def cycle_and_gradient(cls, name, vehicle_type, vehicle_size, cycle_name):
        s = cls(name)

        parameters = inspect.signature(cls.cycle_and_gradient).parameters
        arguments = inspect.currentframe().f_locals
        for key in parameters:
            if key not in ["cls", "name"]:
                s[key] = arguments[key]

        s.cycle, s.gradient = get_standard_driving_cycle_and_gradient(
            vehicle_type, vehicle_size, cycle_name
        )

        assert len(s.cycle) == len(
            s.gradient
        ), "The length of the driving cycle and the gradient must be the same."

        return s

    def compute(self):
        array = xr.DataArray.from_dict(self.array)
        self.curb_mass = array.loc[dict(parameter="glider base mass")] * (
            1 - array.loc[dict(parameter="lightweighting")]
        )

        curb_mass_includes = [
            "fuel mass",  # engine
            "charger mass",  # In an electrical module
            "converter mass",  # Dont really know what it is: probably electrical module
            "inverter mass",  # Same as above
            "power distribution unit mass",  # Should be here: depending on the power distribution module ?
            # Updates with set_components_mass
            "combustion engine mass",
            # Updates with set_components_mass
            "electric engine mass",
            # Updates with set_components_mass
            "powertrain mass",
            "fuel cell stack mass",
            "fuel cell ancillary BoP mass",
            "fuel cell essential BoP mass",
            "battery cell mass",
            "battery BoP mass",
            "fuel tank mass",
        ]

        self.curb_mass += array.loc[dict(parameter=curb_mass_includes)].sum(axis=2)
        self.total_cargo_mass = (
            array.loc[dict(parameter="average_passengers")]
            * array.loc[dict(parameter="average passenger mass")]
            + array.loc[dict(parameter="cargo mass")]
        )
        self.driving_mass = self.curb_mass + self.total_cargo_mass
