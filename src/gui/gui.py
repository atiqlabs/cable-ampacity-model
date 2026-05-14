from PySide6.QtWidgets import (
    QMainWindow,
    QGraphicsScene,
    QGraphicsView,
    QComboBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QWidget,
    QVBoxLayout
)

from PySide6.QtGui import (
    QBrush,
    QPen,
    QColor,
    QPainter
)

from PySide6.QtCore import Qt


class MainWindow(QMainWindow):

    def __init__(
        self,
        cable,
        installation,
        environment,
        engine
    ):

        super().__init__()

        # =====================================
        # Engineering Objects
        # =====================================

        self.cable = cable
        self.installation = installation
        self.environment = environment
        self.engine = engine

        # =====================================
        # Window
        # =====================================

        self.setWindowTitle(
            "IEC 60287 Cable Ampacity GUI"
        )

        self.resize(1000, 700)

        # =====================================
        # Central Widget + Main Layout
        # =====================================

        central_widget = QWidget()

        main_layout = QVBoxLayout(
            central_widget
        )

        # =====================================
        # Graphics Scene + View
        # =====================================

        self.scene = QGraphicsScene()

        self.view = QGraphicsView(
            self.scene
        )

        # Smooth rendering
        self.view.setRenderHint(
            QPainter.Antialiasing
        )

        # =====================================
        # Layer Sequence
        # =====================================

        self.layer_sequence = [
            "Sealed Conductor",
            "SCWB Tape 1",
            "Inner Semi",
            "XLPE",
            "Outer Semi",
            "SCWB Tape 2",
            "Cu Screen",
            "SCWB Tape 3",
            "Al Tape",
            "HDPE Jacket",
            "Graphite"
        ]

        # =====================================
        # Controls
        # =====================================

        control_layout = QHBoxLayout()

        self.layer_dropdown = QComboBox()

        self.layer_dropdown.addItems(
            self.layer_sequence
        )

        self.input_field = QLineEdit()

        self.update_placeholder(
            self.layer_dropdown.currentText()
        )

        self.layer_dropdown.currentTextChanged.connect(
            self.update_placeholder
        )

        self.add_button = QPushButton(
            "Update Layer"
        )

        # =====================================
        # Add Controls
        # =====================================

        control_layout.addWidget(
            QLabel("Layer:")
        )

        control_layout.addWidget(
            self.layer_dropdown
        )

        control_layout.addWidget(
            QLabel("Value:")
        )

        control_layout.addWidget(
            self.input_field
        )

        control_layout.addWidget(
            self.add_button
        )

        # =====================================
        # Add Layouts
        # =====================================

        main_layout.addLayout(
            control_layout
        )

        main_layout.addWidget(
            self.view
        )

        # =====================================
        # Results Section
        # =====================================

        self.ampacity_label = QLabel(
            "Ampacity:"
        )

        self.rac_label = QLabel(
            "AC Resistance:"
        )

        self.t1_label = QLabel(
            "T1:"
        )

        self.t4_label = QLabel(
            "T4 Total:"
        )

        main_layout.addWidget(
            self.ampacity_label
        )

        main_layout.addWidget(
            self.rac_label
        )

        main_layout.addWidget(
            self.t1_label
        )

        main_layout.addWidget(
            self.t4_label
        )

        # =====================================
        # Set Central Widget
        # =====================================

        self.setCentralWidget(
            central_widget
        )

        # =====================================
        # Signals
        # =====================================

        self.add_button.clicked.connect(
            self.add_layer
        )

        # =====================================
        # Initial Draw + Calculation
        # =====================================

        self.draw_cable()

        self.recalculate()

    # =====================================
    # Layer Update
    # =====================================

    def add_layer(self):

        selected_layer = (
            self.layer_dropdown.currentText()
        )

        value_text = (
            self.input_field.text()
        )

        if not value_text:
            return

        try:
            value = float(value_text)

        except ValueError:
            return

        # ---------------------------------
        # Find Layer Index
        # ---------------------------------

        index = self.layer_sequence.index(
            selected_layer
        )

        # ---------------------------------
        # Update Backend Cable Model
        # ---------------------------------

        self.cable.update_layer_value(
            index,
            value
        )

        # ---------------------------------
        # Recalculate Engineering Results
        # ---------------------------------

        self.recalculate()

        # ---------------------------------
        # Redraw Cable
        # ---------------------------------

        self.draw_cable()

        self.input_field.clear()

    # =====================================
    # Placeholder Update
    # =====================================

    def update_placeholder(
        self,
        selected_layer
    ):

        index = self.layer_sequence.index(
            selected_layer
        )

        layer = self.cable.layers[index]

        if layer.is_base:

            self.input_field.setPlaceholderText(
                "Diameter (mm)"
            )

        else:

            self.input_field.setPlaceholderText(
                "Thickness (mm)"
            )

    # =====================================
    # Draw Cable
    # =====================================

    def draw_cable(self):

        self.scene.clear()

        # ---------------------------------
        # Visualization Parameters
        # ---------------------------------

        scale = 2.0

        minimum_visual_thickness = 4

        visual_radii = []

        previous_actual_radius = 0

        cumulative_visual_radius = 0

        # ---------------------------------
        # Compute Visual Radii
        # ---------------------------------

        for layer in self.cable.layers:

            actual_radius = layer.outer_radius

            # ---------------------------------
            # Base Conductor
            # ---------------------------------

            if previous_actual_radius == 0:

                cumulative_visual_radius = (
                    actual_radius * scale
                )

            # ---------------------------------
            # Other Layers
            # ---------------------------------

            else:

                actual_thickness = (
                    actual_radius
                    - previous_actual_radius
                )

                visual_thickness = max(
                    actual_thickness * scale,
                    minimum_visual_thickness
                )

                cumulative_visual_radius += (
                    visual_thickness
                )

            visual_radii.append(
                (
                    cumulative_visual_radius,
                    layer.color
                )
            )

            previous_actual_radius = (
                actual_radius
            )

        # ---------------------------------
        # Draw Outside → Inside
        # ---------------------------------

        for radius, color in reversed(
            visual_radii
        ):

            self.scene.addEllipse(
                -radius,
                -radius,
                2 * radius,
                2 * radius,
                QPen(Qt.black),
                QBrush(QColor(color))
            )

        # ---------------------------------
        # Auto Fit View
        # ---------------------------------

        self.view.fitInView(
            self.scene.itemsBoundingRect(),
            Qt.KeepAspectRatio
        )

    # =====================================
    # Recalculate Engineering Results
    # =====================================

    def recalculate(self):

        results = self.engine.calculate()

        self.ampacity_label.setText(
            f"Ampacity: "
            f"{results.ampacity:.2f} A"
        )

        self.rac_label.setText(
            f"AC Resistance: "
            f"{results.electrical.ac_resistance:.5f} Ω/km"
        )

        self.t1_label.setText(
            f"T1: "
            f"{results.thermal.T1:.3f}"
        )

        self.t4_label.setText(
            f"T4 Total: "
            f"{results.thermal.T4_total:.3f}"
        )