# Copyright (c) 2024, twiinIT - All Rights Reserved
# Safran Aircraft Engine proprietary - See licence file packaged with this code

import numpy as np
from cosapp.systems import System
import pandas as pd
from scipy.constants import g


class Dynamics(System):
    """Dynamics system."""

    def setup(self):
        # inwards/outwards
        self.add_inward("dt", 0.1, unit="s")
        self.add_inward("pos", 0.0, unit="m")
        self.add_inward("velocity", np.array([1.0]), unit="m/s")
        self.add_inward("force", 1.0, unit="N")

        self.add_inward("input_time", 1.0, dtype=(float, np.ndarray))
        self.add_inward("input_velocity", 1.0, dtype=(float, np.ndarray))

        self.add_inward("rolling_resistance_coeff", unit="", valid_range=[0, 1])
        self.add_inward("driving_mass", unit="kg")

        self.add_inward("rho", 1e3, unit="kg/m**3")
        self.add_inward("frontal_area", unit="m**2")
        self.add_inward("drag_coef", unit="")

        self.add_inward("gradient", 1.0, dtype=(float, np.ndarray), unit="rad")

        # outwards
        self.add_outward("rolling_resistance", unit="N")
        self.add_outward("air_resistance", unit="N")
        self.add_outward("gradient_resistance", unit="N")
        self.add_outward("total_resistance", unit="N")

        self.add_outward("motive_energy", unit="W*h")
        # transients
        self.add_outward("acceleration", np.zeros_like(self.velocity), unit="m/s**2")
        # self.add_transient("pos", der="velocity")
        # self.add_rate("acceleration", source="velocity")

    @classmethod
    def from_data(
        cls,
        name: str,
        data=None,
    ):
        s = cls(name)
        if data is not None:
            return
        return s

    @classmethod
    def from_file(
        cls,
        name: str,
        filename: str = None,
    ):
        if filename is not None:
            data = pd.read_excel(filename)
            return cls.from_data(name, data)

    def compute(self):
        # if isinstance(self.input_time, np.ndarray):
        #    time_index = np.where(np.isclose(self.input_time, self.t))[0][0]
        #    self.velocity = self.input_velocity[time_index]
        #    print(time_index, self.velocity)
        if isinstance(self.velocity, np.ndarray) and len(self.velocity) > 1:
            self.acceleration = np.zeros_like(self.velocity)
            self.acceleration[1:-1] = (
                self.velocity[2:] - self.velocity[0:-2]
            ) / self.dt

        self.rolling_resistance = (
            self.driving_mass * self.rolling_resistance_coeff * g * (self.velocity > 0)
        )
        self.air_resistance = (
            self.frontal_area * self.drag_coef * self.rho / 2.0 * self.velocity**2.0
        )
        self.gradient_resistance = (
            self.driving_mass * g * np.sin(self.gradient) * (self.velocity > 0)
        )

        self.inertia = self.acceleration * self.driving_mass

        self.total_resistance = (
            self.rolling_resistance
            + self.air_resistance
            + self.gradient_resistance
            + self.inertia
        )
