"""Application controller for the IEC 60287 desktop workflow.

This controller coordinates the existing engineering models and calculation
engine.  It intentionally has no PySide6 imports: Qt-specific widget work
stays in ``src.gui``.
"""


class MainController:
    """Own the application state used by the GUI.

    This first milestone is a safe integration seam.  It does not change any
    model, calculation, or GUI behaviour yet; subsequent steps will move GUI
    actions here one at a time.
    """

    def __init__(self, cable, installation, environment, engine):
        self.cable = cable
        self.installation = installation
        self.environment = environment
        self.engine = engine

    def calculate_results(self):
        """Return the latest ampacity results from the existing engine."""
        return self.engine.calculate()
    
    def update_layer(self, layer_name, value_text): # take values from drop down

        if not value_text: # Input Validation
            raise ValueError("Input field is empty. Please enter a value")
        
        try:
            value = float(value_text)
        except ValueError:
            raise ValueError("Invalid input. Please enter a numeric value.")
        
        if value <= 0:
            raise ValueError("Invalid input. Please enter a positive value")
        
        # Find the selected layer in the Cable model.
        # The GUI passes only the layer name.
        layer_names = [layer.name for layer in self.cable.layers] 
        index = layer_names.index(layer_name)

        self.cable.update_layer_value(index, value)

        return self.calculate_results()

