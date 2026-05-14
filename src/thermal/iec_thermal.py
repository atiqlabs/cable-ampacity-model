# This module finds out the thermal properties of Cable according to IEC 60287-2-1:2023
# The formula used are from the IEC standards

import math
from src.standards.iec_constants import DUCT_MATERIALS

from src.thermal.internal import InternalThermalResistance
from src.thermal.air_gap import AirGapThermalResistance
from src.thermal.duct import DuctThermalResistance
from src.thermal.external import ExternalThermalResistance
from src.thermal.correction_factors import ThermalCorrectionFactors



class IECThermal:

    # -----------------------------------------------
    # ---INTERNAL THERMAL RESISTANCE (T1,T2,T3)------
    #-----------------------------------------------

    def __init__(self, cable, installation, environment):
        #self.cable = cable
        self.installation = installation
        self.environment = environment

        self.internal = InternalThermalResistance(cable)

        self.air_gap = AirGapThermalResistance(cable)

        self.duct = DuctThermalResistance(installation)

        self.external = ExternalThermalResistance(cable,installation,environment)


        self.correction = ThermalCorrectionFactors(installation)
# ------------------------------------------------------------
#---EXTERNAL THERMAL RESISTANCE TO CABLE (T4)-----------------
#-------------------------------------------------------------
    def thermal_resistance_T4_concrete(self):
        rho = DUCT_MATERIALS["CONCRETE"]["thermal_resistivity"]

        # assume outer radius of duct bank (temporary approximation)
        D_duct = self.installation.duct.outer_diameter / 1000  # m
        D_concrete = D_duct * 2  # simple assumption (expand later)

        return (rho / (2 * math.pi)) * math.log(D_concrete / D_duct)

    def thermal_resistance_T4_total(self):

        if self.installation.duct is not None:
            return (
                self.air_gap.thermal_resistance_T4_air_gap()
                + self.duct.thermal_resistance_T4_duct()
                + self.external.thermal_resistance_T4_external()
                + self.correction.thermal_resistance_T4_backfill_concrete()
            )
        
        else:
            return self.thermal.thermal_resistance_T4_soil()
    
    def ampacity(self,R_ac):
        theta_max = self.environment.temperature   # conductor temp
        theta_ambient = 20  # assume for now (we will improve later)

        delta_theta = theta_max - theta_ambient

        T_total = (
            self.internal.thermal_resistance_T1()
            + self.internal.thermal_resistance_T2()
            + self.internal.thermal_resistance_T3()
            + self.thermal_resistance_T4_total()
        )

        if T_total == 0:
            raise ValueError("Thermal resistance is zero")
        
        # 🔥 FIX: convert Ω/km → Ω/m
        R_ac_m = R_ac / 1000
        
        return math.sqrt(delta_theta / (R_ac_m * T_total))

