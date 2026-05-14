"""
Thermal resistance of air space between cable and duct.

Applicable to:
    - duct installations
    - concrete duct banks
"""

class AirGapThermalResistance:

    """
    Calculates thermal resistance of air between cable
    and duct wall according to IEC 60287.
    """

    def __init__(self, cable):
        self.cable = cable

    def thermal_resistance_T4_air_gap(self):

        U = 1.87
        V = 0.312
        Y = 0.0037

        theta_m = 75  # mean temp from PDF
        d_cable = self.cable.layers[-1].diameter  # meters

        return U / (1 + 0.1 * (V + Y * theta_m) * d_cable)
    
    