# This module finds the Electrical properties of Cable according to IEC 60287-1-1:2023
# Also it will calculate the losses in the cable (Not done yet)

import math
from src.standards.iec_constants import *
from src.standards.iec_inputs import *

class IEC60287:
    def __init__(self,cable, installation, environment, frequency=DEFAULT_FREQUENCY, use_geometric_area = False):
        self.cable=cable
        self.f=frequency
        self.use_geometric_area = use_geometric_area  # in future we will incorporate this value in GUI and pass it here
        self.installation = installation
        self.environment = environment

    def get_conductor(self): # this find conductor layer.
        for layer in self.cable.layers:
            if layer.is_base:
                return layer
            
    def get_conductor_area(self): # extract conductor area from what user enter(1200mm^2) or find it from formula let see in future what to use.

        if self.use_geometric_area: # use geometry i.e use conductor diameter, lets see whether we can use in future or not
            conductor = self.get_conductor()
            d_mm = conductor.value #diameter in mm
            area_mm2 = math.pi*(d_mm**2)/4 # area formula
        else: #  i.e use 1200mm2 as area, this has been used by manufacturer.
            area_mm2 = self.cable.area_mm2
        return area_mm2 * 1e-6 # convert mm2 to m2
    
    def get_conductor_diameter(self):
        conductor = self.get_conductor()

        return conductor.value/1000 # converts mm to meter and return
    
    def dc_resistance(self): # this method finds the dc resistance of the conductor

        temperature = self.environment.temperature

        conductor = self.get_conductor()
        material = conductor.material

        rho20 = material.resistivity_20
        alpha = material.temp_coefficient

        if rho20 is None or alpha is None:
            raise ValueError("Material data missing for conductor!")
        
        # area
        A = self.get_conductor_area()

        # R20 (Ω/m)
        R20 = rho20 / A  # multiply by 1.05 to get the results close to in the pdf report. the resistivity used there is i think value is higher

        # convert to Ω/km
        R20_km = R20 * 1000

        # temperature correction
        R = R20_km * (1 + alpha * (temperature - 20))

        return R

    def skin_effect(self):

        temperature = self.environment.temperature
        props = self.get_ks_kp()
        ks = props["ks"]

        R_dc = self.dc_resistance()
        R_dc_m = R_dc/1000 #convert km to m as per calculations used in Riyadh cables

        xs2 = (8 * math.pi * self.f * 1e-7 * ks) / R_dc_m
        xs4 = xs2 ** 2

        ys = xs4 / (192 + 0.8 * xs4) 

        return ys  
    
    def proximity_effect(self):

        temperature = self.environment.temperature
        props = self.get_ks_kp()
        kp = props["kp"]

        R_dc = self.dc_resistance()
        R_dc_m = R_dc / 1000 #convert Km to meter

        # Step 1: base yp' (IEC)
        xp2 = (8 * math.pi * self.f * kp * 1e-7) / R_dc_m  # Section 5.1.5 IEC 60287-1-1-2023
        xp4 = xp2 ** 2

        yp_base = xp4 / (192 + 0.8 * xp4)

        # Step 2: geometry correction
        dc = self.get_conductor_diameter()  # diameter of conductor in meters
        s = self.installation.spacing / 1000       # spacing of the cables mm → meters

        if s == 0:
            raise ValueError("Spacing cannot be zero")
        
        ratio2 = (dc / s) ** 2 # this power of the ratio used. see in formula
        yp = yp_base * ratio2 * (0.312 * ratio2 + 1.18 / (yp_base + 0.27)) # formula for 03 core cable

        return yp

    
    def get_ks_kp(self):
        conductor = self.get_conductor()
        material_name = conductor.material.name
        conductor_type = self.cable.conductor_type
        conductor_insulation_system = self.cable.conductor_insulation_system

        key = (material_name,conductor_type,conductor_insulation_system)

        if key not in IEC_CONDUCTOR_TABLE02:
            raise ValueError(f"IEC Table 02 values not defined for {key}")
        return IEC_CONDUCTOR_TABLE02[key]
    
    def ac_resistance(self): # to find AC resistance at operating temperature
        
        temperature = self.environment.temperature
        R_dc = self.dc_resistance()

        ys = self.skin_effect()
        yp = self.proximity_effect()

        R_ac = R_dc * (1 + ys + yp) # Section 5.1.6 of IEC 60287-1-1-2023

        return R_ac
    

    



