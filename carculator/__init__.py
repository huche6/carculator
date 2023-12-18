"""Carculator init file.

List of all submodules.

Submodules
==========

.. autosummary::
    :toctree: _autosummary

"""
from pathlib import Path

from carculator_utils.array import fill_xarray_from_input_parameters
from carculator_utils.driving_cycles import get_standard_driving_cycle_and_gradient

from .car_input_parameters import CarInputParameters
from .inventory import InventoryCar
from .model import CarModel

__all__ = (
    "CarInputParameters",
    "fill_xarray_from_input_parameters",
    "CarModel",
    "InventoryCar",
    "get_standard_driving_cycle_and_gradient",
)
__version__ = (1, 8, 5)


DATA_DIR = Path(__file__).resolve().parent / "data"
