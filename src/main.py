import sys
from src.standards.iec_constants import *
from src.models.installation import Installation
from src.models.environment import Environment
from src.models.duct import Duct
from src.models.concrete_duct_bank import ConcreteDuctBank
from src.calculations.ampacity_engine import AmpacityEngine
from src.utilis.display_results import display_results

from PySide6.QtWidgets import QApplication
from src.models.cable import Cable
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

    concrete_duct_bank = ConcreteDuctBank() # we will populate it later. from user

    installation = Installation(
        formation = "flat",
        spacing = 400, # in mm
        depth = 1600, # in mm  # previously 1450
        duct = duct,
        concrete_duct_bank=concrete_duct_bank
    )

    environment = Environment(
        temp_mode = "normal"
    )

    engine = AmpacityEngine(cable,installation,environment)

    results = engine.calculate()  # you can print results like results.ampacity etc
    display_results(results) # display results and is imported from utilis


    #-------------------------------------------------
    #--------GUI Launch -----------------------------
    #------------------------------------------------

    app = QApplication(sys.argv)  # Uncomment this for GUI
    window = MainWindow(cable,
                        installation,
                        environment,
                        engine
                        )
    window.show()
    sys.exit(app.exec())




if __name__ == "__main__":
    main()
 