from carculator.systems.fleet import Fleet
from cosapp.drivers import NonLinearSolver, EulerExplicit
import numpy as np


class TestProperties:
    def test_curb_mass_electrical(self):
        # Initialize system
        fleet = Fleet("fleet", sizes="Medium", cycle="WLTC", powertrains="BEV")

        fleet.vec_0.glider.mass = 1350.0
        fleet.vec_0.powertrain.type = "BEV"
        fleet.vec_0.powertrain.powertrain_specs.power_to_mass_ratio = 80.0
        fleet.vec_0.powertrain.powertrain_specs.powertrain_mass_per_power = 0.4
        fleet.vec_0.powertrain.powertrain_specs.powertrain_fixed_mass = 34.5
        fleet.vec_0.curb_mass = 1450

        # First run to init curb_mass
        fleet.vec_0.run_once()

        # NonLinearSolver
        fleet.vec_0.drivers.clear()

        time_driver = fleet.vec_0.add_driver(
            EulerExplicit("euler", dt=1, time_interval=[0, 10])
        )

        # solver = time_driver.add_child(NonLinearSolver("solver", max_iter=50, tol=1e-6))
        # solver.extend(fleet.vec_0.design_methods["scale_mass"])

        time_driver.set_scenario(
            name="mission",
            values={
                "vehicle_dynamic.velocity": np.repeat(
                    np.sin(np.linspace(-np.pi, np.pi, 200)) * 20 + 50, 5
                )
            },
        )

        fleet.run_drivers()

        assert np.isclose(fleet.vec_0.curb_mass, fleet.vec_0.mass_out.mass)
        assert np.isclose(
            fleet.vec_0.driving_mass,
            fleet.vec_0.curb_mass + fleet.vec_0.vehicle_weight.total_cargo_mass,
        )
