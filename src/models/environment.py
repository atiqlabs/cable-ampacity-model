from src.standards.iec_constants import *

class Environment:
    def __init__(self, temp_mode = "normal", temperature = None, soil_resistivity = 1.2):

        if temperature is not None:  # If user gives custom temperature → use it
            self.temperature = temperature
            self.temp_mode = temp_mode

        else: # Otherwise use predefined mode which are defined in iec_constants.py
            if temp_mode not in OPERATING_TEMPERATURES:
                raise ValueError(f"Invalid temperature mode: {temp_mode}")
            
            self.temperature = OPERATING_TEMPERATURES[temp_mode]
            self.temp_mode = temp_mode

        self.soil_resistivity = soil_resistivity # in degree C.m/Watt or K.m/Watt