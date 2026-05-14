"""
External thermal resistance between installation system
and surrounding soil.
"""

import math
from src.standards.iec_constants import DUCT_MATERIALS


class ExternalThermalResistance:

    """
    Calculates external thermal resistance to surrounding soil.
    """

    def __init__(self, cable, installation, environment):
        self.cable = cable
        self.installation = installation
        self.environment = environment

    def thermal_resistance_T4_external(self):

        rho_c = DUCT_MATERIALS["CONCRETE"]["thermal_resistivity"]
        L = self.installation.depth / 1000
        Do = self.installation.duct.outer_diameter / 1000
        s = self.installation.spacing / 1000

        u = 2 * L / Do

        term1 = math.log(u + math.sqrt(u**2 - 1))
        term2 = math.log(1 + (2 * L / s)**2)

        return (rho_c / (2 * math.pi)) * (term1 + term2)

    def thermal_resistance_T4_soil(self):
        rho = self.environment.soil_resistivity # K.m/W
        D = self.cable.layers[-1].diameter # Cable outer diameter (last layer)
        depth = self.installation.depth/1000 # mm to m
        return (rho / (2 * math.pi)) * math.log(2 * depth / D)