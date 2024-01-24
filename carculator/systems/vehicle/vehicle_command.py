from cosapp.base import System


class VehicleCommand(System):
    def setup(self):
        self.add_inward("city_speed", 50.0 * 1e3 / 3600, unit="m/s")

        self.add_inward("country_speed", 90.0 * 1e3 / 3600, unit="m/s")

        self.add_inward("highway_speed", 130.0 * 1e3 / 3600, unit="m/s")
