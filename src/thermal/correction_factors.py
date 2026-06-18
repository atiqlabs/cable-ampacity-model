"""
Thermal correction factors for special installation systems.

Currently includes:
    - concrete duct bank backfill correction
"""

import math


class ThermalCorrectionFactors:

    """
    Calculates thermal correction factors according
    to IEC 60287.
    """

    def __init__(self, installation):
        self.installation = installation

    def thermal_resistance_T4_backfill_concrete(self):

        bank = self.installation.concrete_duct_bank

        N = bank.num_cables
        rho_bf = bank.backfill_resistivity   # backfill (temporary, from PDF)
        rho_c = bank.concrete_resistivity    # concrete

        # STEP 2: equivalent radius according to clause 4.2.7 of IEC 60287-2-1:2023

        x = bank.width   # the shorter/width in this case side in meters
        y = bank.height   # the longer side in meters

        z = bank.top_cover   # above duct bank

        term1 = ((x / (2 * y)) ** ((4 / math.pi) - (x / y)))
        term2 = math.log(1 + (y**2 / x**2))
        term3 = math.log(x / 2)

        rb = math.exp(term1 * term2 + term3)

        # STEP 3: depth to center
       # LG = self.installation.depth / 1000
        LG = z + y/2
        # STEP 3: compute u
        u = LG / rb

        return (N / (2 * math.pi)) * (rho_bf - rho_c) * math.log(u + math.sqrt(u**2 - 1))