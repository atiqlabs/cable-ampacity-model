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
