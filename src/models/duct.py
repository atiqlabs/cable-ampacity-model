from src.standards.iec_constants import *

class Duct:
    def __init__(self,inner_diameter,outer_diameter,material = "PVC"):
        self.inner_diameter = inner_diameter
        self.outer_diameter = outer_diameter
        self.material = material

        if material not in DUCT_MATERIALS: # validate the material is present in the iec_constansts.DUCT_MATERIALS
            raise ValueError(f"Unknown duct material: {material}")
        
        self.thermal_resistivity = DUCT_MATERIALS[material]["thermal_resistivity"]