from iec_constants import *

class Installation:
    def __init__(self,formation = "flat", spacing = 400, depth = 1450, duct = None):
        self.formation = formation

        if spacing == 0: # control for spacing
            raise ValueError(f"Invalid spacing:spacing should be greator than {spacing}")
        else:
            self.spacing = spacing # in mm


        self.depth = depth # depth from the surface of the ground to the group center in mm
        self.duct = duct # we will take the properties of duct from user. and note it is an object of class Duct.

class Environment:
    def __init__(self, temp_mode = "normal", temperature = None, soil_resistivity = 1.0):

        if temperature is not None:  # If user gives custom temperature → use it
            self.temperature = temperature
            self.temp_mode = temp_mode

        else: # Otherwise use predefined mode which are defined in iec_constants.py
            if temp_mode not in OPERATING_TEMPERATURES:
                raise ValueError(f"Invalid temperature mode: {temp_mode}")
            
            self.temperature = OPERATING_TEMPERATURES[temp_mode]
            self.temp_mode = temp_mode

        self.soil_resistivity = soil_resistivity # in degree C.m/Watt or K.m/Watt

class Duct:
    def __init__(self,inner_diameter,outer_diameter,material = "PVC"):
        self.inner_diameter = inner_diameter
        self.outer_diameter = outer_diameter
        self.material = material

        if material not in DUCT_MATERIALS: # validate the material is present in the iec_constansts.DUCT_MATERIALS
            raise ValueError(f"Unknown duct material: {material}")
        
        self.thermal_resistivity = DUCT_MATERIALS[material]["thermal_resistivity"]
        



