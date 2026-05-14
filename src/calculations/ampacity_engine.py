"""
High-level IEC 60287 ampacity calculation engine.

Coordinates:
    - electrical calculations
    - thermal calculations
    - ampacity evaluation

This engine acts as the application-level calculation
workflow used by:
    - command-line studies
    - GUI
    - reports
    - future automation workflows
"""

from src.electrical.iec_electrical import IEC60287
from src.thermal.iec_thermal import IECThermal
from src.models.results import (ElectricalResults,ThermalResults,AmpacityResults)

class AmpacityEngine:
    def __init__(self, cable, installation, environment):
        self.electrical = IEC60287(cable, installation, environment) # electrical
        self.thermal = IECThermal(cable, installation, environment) # thermal

    def calculate(self): # because GUi needs one calculation call
        Rdc = self.electrical.dc_resistance() # DC resistance

        ys = self.electrical.skin_effect() # finds ys

        yp = self.electrical.proximity_effect()

        R_ac = self.electrical.ac_resistance() # finds Rac

        T1 = self.thermal.internal.thermal_resistance_T1()

        T2 = self.thermal.internal.thermal_resistance_T2()
        T3 = self.thermal.internal.thermal_resistance_T3()

        T4_duct = self.thermal.duct.thermal_resistance_T4_duct()

        T4_total = self.thermal.thermal_resistance_T4_total()

        I = self.thermal.ampacity(R_ac)

        electrical_results = ElectricalResults(dc_resistance=Rdc,skin_effect=ys,
                                               proximity_effect=yp,ac_resistance=R_ac)
        
        thermal_results = ThermalResults(T1=T1, T2=T2, T3=T3,
                                         T4_duct=T4_duct,T4_total=T4_total)
        
        return AmpacityResults(
                               electrical=electrical_results,
                               thermal=thermal_results,
                               ampacity=I
                               )

