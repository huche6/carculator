from cosapp.base import System


class Powertrain(System):
    def setup(self):
        self.add_inward("type", None, dtype=(list, str))
        self.add_inward("mass", None)
