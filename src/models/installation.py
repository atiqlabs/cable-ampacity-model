from src.standards.iec_constants import *

class Installation:
    def __init__(self,formation = "flat", spacing = 400, depth = 1600, duct = None, concrete_duct_bank=None):
        self.formation = formation

        if spacing == 0: # control for spacing
            raise ValueError(f"Invalid spacing:spacing should be greator than {spacing}")
        else:
            self.spacing = spacing # in mm


        self.depth = depth # depth from the surface of the ground to the group center in mm
        self.duct = duct # we will take the properties of duct from user. and note it is an object of class Duct.

        self.concrete_duct_bank = concrete_duct_bank