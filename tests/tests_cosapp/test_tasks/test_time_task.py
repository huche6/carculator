from cosapp_utils.tasks import TimeDriverTask, DesignTask
from pathlib import Path
import numpy as np
from carculator.systems.fleet import Fleet
from cosapp.recorders import DataFrameRecorder


class TestTimeDriver:
    def test_run_once(self):
        task = TimeDriverTask("td")

        data_path = Path(__file__).parent / "vecto_cycle.txt"
        velocity = np.loadtxt(data_path)
        task.init = {
            "vec_0.vehicle_dynamic.input_velocity": velocity[:, 1],
            "vec_0.vehicle_dynamic.input_time": velocity[:, 0],
        }
        task.dt = 1.0
        task.time_max = 999

        task.s_in.system = Fleet("sys")

        task.run_once()

        sys = task.s_out.system

        assert sys.vec_0.vehicle_dynamic.velocity == velocity[:, 1][-1]

    def test_design_then_time(self):
        design = DesignTask("design_task_mass")
        design.equation = "vec_0.mass_out.mass - vec_0.curb_mass == 0"
        design.unknown = "vec_0.curb_mass"

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

        design.s_in.system.vec_0.powertrain.electrical_powertrain.combustion_power_share = (
            0.0
        )

        design.run_once()

        assert (
            design.s_out.system.vec_0.curb_mass
            == design.s_out.system.vec_0.mass_out.mass
        )

        task = TimeDriverTask("td")

        data_path = Path(__file__).parent / "vecto_cycle.txt"
        velocity = np.loadtxt(data_path)
        task.init = {
            "vec_0.vehicle_dynamic.velocity": velocity[:, 1],
            # "vec_0.vehicle_dynamic.input_time": velocity[:, 0],
        }
        task.system.vec_0.vehicle_dynamic.dt = 1.0
        task.time_max = 999

        task.s_in.system = design.s_out.system

        task.run_once()

        sys = task.s_out.system

        print(
            task.data_out["vec_0.vehicle_dynamic.velocity"].head(10),
            task.data_out["vec_0.vehicle_dynamic.pos"].head(10),
        )

        assert sys.vec_0.curb_mass == sys.vec_0.mass_out.mass
        assert sys.vec_0.vehicle_dynamic.velocity == velocity[:, 1][-1]
