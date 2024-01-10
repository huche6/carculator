from cosapp.base import Port


class Mass(Port):
    def setup(self):
        self.add_variable("mass", 1.0, desc="total mass without passengers and cargo.")
