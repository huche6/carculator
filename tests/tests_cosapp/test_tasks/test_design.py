import pytest
from cosapp.drivers import NonLinearSolver
from carculator.systems.fleet import Fleet
from pathlib import Path
import numpy as np

from cosapp_utils.tasks import DesignTask


class TestDesign:
    def test_design_mass(self):
        design = DesignTask("design_task_mass")
        # design.equation = "vec_0.mass_out.mass - vec_0.curb_mass == 0"
        # design.unknown = "vec_0.curb_mass"

        # Initialize system
        design.s_in.system = Fleet(
            "fleet", sizes="Medium", cycle="WLTC", powertrains="BEV"
        )

        design.s_in.system.vec_0.glider.mass = 1350.0
        design.s_in.system.vec_0.powertrain.type = "BEV"
        design.s_in.system.vec_0.powertrain.powertrain_specs.power_to_mass_ratio = 80.0
        design.s_in.system.vec_0.powertrain.powertrain_specs.powertrain_mass_per_power = (
            0.4
        )
        design.s_in.system.vec_0.powertrain.powertrain_specs.powertrain_fixed_mass = (
            34.5
        )
        design.s_in.system.vec_0.curb_mass = 1450

        design.run_once()

        assert (
            design.s_out.system.vec_0.curb_mass
            == design.s_out.system.vec_0.mass_out.mass
        )

    def test_design_mass_and_velocity(self):
        design = DesignTask("design_task_mass")
        # design.equation = "vec_0.mass_out.mass - vec_0.curb_mass == 0"
        # design.unknown = "vec_0.curb_mass"

        # Initialize system
        design.s_in.system = Fleet(
            "fleet", sizes="Medium", cycle="WLTC", powertrains="BEV"
        )

        design.s_in.system.vec_0.glider.mass = 1350.0
        design.s_in.system.vec_0.powertrain.type = "BEV"
        design.s_in.system.vec_0.powertrain.powertrain_specs.power_to_mass_ratio = 80.0
        design.s_in.system.vec_0.powertrain.powertrain_specs.powertrain_mass_per_power = (
            0.4
        )
        design.s_in.system.vec_0.powertrain.powertrain_specs.powertrain_fixed_mass = (
            34.5
        )
        design.s_in.system.vec_0.curb_mass = 1450

        data_path = Path(__file__).parent / "vecto_cycle.txt"
        velocity = np.loadtxt(data_path)

        design.s_in.system.vec_0.vehicle_dynamic.velocity = velocity[:, 1]
        design.s_in.system.vec_0.vehicle_dynamic.dt = 15.0

        design.run_once()
