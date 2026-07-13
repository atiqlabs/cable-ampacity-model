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
    
    def update_installation(self,spacing_text, depth_text): # For Cable Installation Parameters. Module 03
        
        if not spacing_text or not depth_text:
            raise ValueError("Input fields are empty. Please enter values.")
        
        try:
            spacing = float(spacing_text)
            depth = float (depth_text)

        except ValueError:
            raise ValueError("Invalid input. Please enter numeric values.")
        
        if spacing <= 0 or depth <= 0:
            raise ValueError("Invalid input. Please enter positive values.")
        
        self.installation.spacing = spacing
        self.installation.depth = depth

        return self.calculate_results() 
    
    def update_duct_bank(
                        self, 
                        num_cables_text,
                        width_text,
                        height_text,
                        top_cover_text,
                        concrete_resistivity_text,
                        backfill_resistivity_text,
                        ):
        
        try:
            num_cables = int(num_cables_text)
            width = float(width_text)
            height = float(height_text)
            top_cover = float(top_cover_text)
            concrete_resistivity = float(concrete_resistivity_text)
            backfill_resistivity = float(backfill_resistivity_text) 

        except ValueError:
            raise ValueError("Invalid input. Please enter numeric values.")   

        if (
            num_cables <= 0
            or width <= 0
            or height <= 0
            or top_cover <= 0
            or concrete_resistivity <= 0
            or backfill_resistivity <= 0
            ):
            raise ValueError("Invalid input. Please enter positive values.")
        

        bank = self.installation.concrete_duct_bank

        bank.num_cables = num_cables
        bank.width = width
        bank.height = height
        bank.top_cover = top_cover
        bank.concrete_resistivity = concrete_resistivity
        bank.backfill_resistivity = backfill_resistivity

        return self.calculate_results()
    
    def get_layer_input_placeholder(self, layer_name):
        for layer in self.cable.layers:
            if layer.name == layer_name:
                if layer.is_base:
                    return "Diameter (mm)"
                return "Thickness (mm)"
            
        raise ValueError(f"Unknown cable layer: {layer_name}")
        
