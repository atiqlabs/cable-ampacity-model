"""
Thermal resistance of duct materials surrounding the cable.
"""

import math


class DuctThermalResistance:

    """
    Calculates thermal resistance through duct wall.
    """

    def __init__(self, installation):
        self.installation = installation

    def thermal_resistance_T4_duct(self): # Thermal resistance of the duct (or pipe) itself. Clasue 4.2.6.4- IEC 60287-2-1


        duct = self.installation.duct

        if duct is None:
            return 0
        
        rho = duct.thermal_resistivity

        D_out = duct.outer_diameter
        D_in = duct.inner_diameter

        return (rho / (2 * math.pi)) * math.log(D_out / D_in) # see Section 4.2.6.4 of IEC 60287-2-1