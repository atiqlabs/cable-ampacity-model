# This module finds out the thermal properties of Cable according to IEC 60287-2-1:2023
# The formula used are from the IEC standards

import math


class IECThermal:

    # -----------------------------------------------
    # ---INTERNAL THERMAL RESISTANCE (T1,T2,T3)------
    #-----------------------------------------------

    def __init__(self, cable, installation, environment):
        self.cable = cable
        self.installation = installation
        self.environment = environment

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
                
                D_out = current.diameter/1000 # convert mm to m
                D_in = previous.diameter/1000 # convert mm to m

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
    
# ------------------------------------------------------------
#---EXTERNAL THERMAL RESISTANCE TO CABLE (T4)-----------------
#-------------------------------------------------------------
    def thermal_resistance_T4_air(self):
        pass
    
    
    def thermal_resistance_T4_duct(self): # Thermal resistance of the duct (or pipe) itself. Clasue 4.2.6.4- IEC 60287-2-1


        duct = self.installation.duct

        if duct is None:
            return 0
        
        rho = duct.thermal_resistivity

        D_out = duct.outer_diameter
        D_in = duct.inner_diameter

        return (rho / (2 * math.pi)) * math.log(D_out / D_in) # see Section 4.2.6.4 of IEC 60287-2-1

    def thermal_resistance_T4_external(self):
        pass

    def thermal_resistance_T4_backfill(self):
        pass

    def thermal_resistance_T4_soil(self):
        pass

    def thermal_resistance_T4_total(self):
        return (
            self.thermal_resistance_T4_air()
            + self.thermal_resistance_T4_duct()
            + self.thermal_resistance_T4_external()
            + self.thermal_resistance_T4_backfill()
            + self.thermal_resistance_T4_soil()
        )

