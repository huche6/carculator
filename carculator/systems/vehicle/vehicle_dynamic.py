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
        self.add_inward("speed", 50.0, unit="m/s")
        self.add_inward("force", 1.0, unit="N")

        self.add_inward("input_time", 1.0, dtype=(float, np.ndarray))
        self.add_inward("input_velocity", 1.0, dtype=(float, np.ndarray))

        self.add_inward("rolling_resistance_coeff", unit="", valid_range=[0, 1])
        self.add_inward("driving_mass", unit="kg")

        self.add_inward("rho", 1e3, unit="kg/m**3")
        self.add_inward("frontal_area", unit="m**2")
        self.add_inward("drag_coef", unit="")

        self.add_inward("gradient", 1.0, dtype=(float, np.ndarray), unit="rad")

        self.add_inward("engine_efficiency", unit="")
        self.add_inward("transmission_efficiency", unit="")

        # outwards
        self.add_outward("rolling_resistance", unit="N")
        self.add_outward("air_resistance", unit="N")
        self.add_outward("gradient_resistance", unit="N")
        self.add_outward("total_resistance", unit="N")
        self.add_outward("inertia", unit="N")

        self.add_outward("motive_energy", unit="W*h")
        # transients
        self.add_outward("acceleration", np.zeros_like(self.speed), unit="m/s**2")
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
        self.rolling_resistance = (
            self.driving_mass * self.rolling_resistance_coeff * g * (self.speed > 0)
        )
        self.air_resistance = (
            self.frontal_area * self.drag_coef * self.rho / 2.0 * self.speed**2.0
        )
        self.gradient_resistance = (
            self.driving_mass * g * np.sin(self.gradient) * (self.speed > 0)
        )

        self.inertia = self.acceleration * self.driving_mass

        self.total_resistance = (
            self.rolling_resistance
            + self.air_resistance
            + self.gradient_resistance
            + self.inertia
        )

        # self.motive_energy_at_wheels = np.maximum(self.total_resistance, 0.0)
