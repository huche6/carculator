from cosapp.base import System
from typing import List
import numpy as np


class Engine(System):
    def setup(self):
        self.add_inward("vehicle_type", None, dtype=str)
        self.add_inward("vehicle_size", None, dtype=list)
        self.add_inward("powertrains", None, dtype=list)
        self.add_inward("cycle", None, dtype=(str, np.ndarray))
        self.add_inward("gradient", None, dtype=(str, np.ndarray))
