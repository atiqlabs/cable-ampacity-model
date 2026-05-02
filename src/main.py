import sys
from src.electrical.iec_electrical import IEC60287
from src.standards.iec_constants import *
from src.standards.iec_inputs import *
from src.thermal.iec_thermal import IECThermal

from PySide6.QtWidgets import QApplication
from src.models.cable import Cable, Material
from src.gui.gui import MainWindow

def main():

    cable = Cable( # following are all inputs that should be taken from user
        cable_type="Cu/XLPE/CWS/LAT/HDPE",
        size="1200 mm²",
        voltage="110 kV",
        standard="11-TMSS-02",
        conductor_type="Round/Milliken", # Case Sensitive, you take input from user like this and display it in future GUI. these are mapped to simples name in 
        conductor_insulation_system="Fluid/Paper/PPL", # Case Sensitive 
    )

    duct = Duct(
        inner_diameter = 200, # in mm
        outer_diameter = 225, # in mm
        material = "PVC"
    )

    installation = Installation(
        formation = "flat",
        spacing = 400, # in mm
        depth = 1450, # in mm
        duct = duct
    )

    environment = Environment(
        temp_mode = "normal"
    )
    
    print("Layer Validations")
    for layer in cable.layers:
        print(layer.name, round(layer.diameter,2), " ---- ", layer.layer_type)

    iec = IEC60287(cable, installation, environment)

    conductor = iec.get_conductor()

    print(conductor.name)
    print(conductor.value)

    R = iec.dc_resistance() # DC resistance
    print("DC Resistance (\u03A9/km):",round(R,5))

    ys = iec.skin_effect()
    print("Skin effect ys:", round(ys,5))

    yp = iec.proximity_effect()
    print("Proximity effect yp:", round(yp,5))

    R_ac = iec.ac_resistance()
    print("AC Resistance (Ω/km):", round(R_ac,5))

    thermal = IECThermal(cable, installation, environment)
    T1 = thermal.thermal_resistance_T1()
    print("T1 =", round(T1, 3))

    T2 = thermal.thermal_resistance_T2()
    print("T2 =", round(T2, 3))

    T3 = thermal.thermal_resistance_T3()
    print("T3 =", round(T3, 3))

    T4_duct = thermal.thermal_resistance_T4_duct()
    print("T4 (duct) =", round(T4_duct, 3))

    T4_total = thermal.thermal_resistance_T4_total()
    print("T4 total =", round(T4_total, 3))

    

    R_ac = iec.ac_resistance()
    I = thermal.ampacity(R_ac)
    print("Ampacity (A):", I)

    # Un comment this if you want to see the conductor.

    """app = QApplication(sys.argv)  # Uncomment this for GUI
    window = MainWindow(cable)
    window.show()
    sys.exit(app.exec())"""




if __name__ == "__main__":
    main()
 