"""
Internal thermal resistances of the cable according to IEC 60287-2-1.

This module contains:
    - T1 : conductor to sheath
    - T2 : sheath to armour
    - T3 : outer jacket

These thermal resistances depend only on cable construction
and are independent of installation method.
"""

import math


class InternalThermalResistance:
    """
    Calculates internal thermal resistances of cable construction
    according to IEC 60287-2-1.
    """

    def __init__(self, cable):
        self.cable = cable

    def thermal_resistance_T1(self): # This method find thermal resistance between conductor and Sheath(Al here)
        T1 = 0
        layers = self.cable.layers

        for i in range(1, len(layers)):

            current = layers[i]
            previous = layers[i-1]

            # STOP at Aluminium sheath
            if current.layer_type == "sheath":  # sheath is the 1st outer protective layer after insulation. dont confuse it with screen because the thermal model treats it different.
                break

            if current.layer_type == "jacket": # let say a cable has no sheath, so it will stop at jacket
                break

            rho = current.material.thermal_resistivity

            if rho is None:
                continue

            D_out = current.diameter
            D_in = previous.diameter

            T1 += (rho / (2 * math.pi)) * math.log(D_out / D_in)  # See clause 4.1.3 of IEC 60287-2-1:2023.

        return T1
    
    def thermal_resistance_T2(self): # in our case T2 = 0
        T2 = 0
        layers = self.cable.layers

        for i in range(1,len(layers)):

            current = layers[i]
            previous = layers[i-1]

            if current.layer_type == "armour":

                rho = current.material.thermal_resistivity

                if rho is None:
                    return 0
                
                D_out = current.diameter #  /1000 removed
                D_in = previous.diameter # /1000 removed

                return (rho / (2 * math.pi)) * math.log(D_out / D_in)
        
        return 0
    
    def thermal_resistance_T3(self): # finds T3 between sheath and HDPE Jacket.
        T3 = 0
        layers = self.cable.layers

        for i in range(1,len(layers)):

            current = layers[i]
            previous = layers[i-1]

            # find HDPE Jacket and extract their properties

            if current.layer_type == "jacket":

                rho = current.material.thermal_resistivity

                D_out = current.diameter
                D_in = previous.diameter

                T3 = (rho / (2 * math.pi)) * math.log(D_out / D_in)

                return T3
        return 0