from PySide6.QtWidgets import (
    QMainWindow,
    QGraphicsScene,
    QGraphicsView,
    QComboBox,
    QLineEdit,
    QPushButton,
    QLabel,
    QGridLayout,
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

    def __init__(self, cable, installation, environment, engine):
        super().__init__()

        self.cable = cable
        self.installation = installation
        self.environment = environment
        self.engine = engine

        self.setWindowTitle("IEC 60287 Cable Ampacity GUI")
        self.resize(1000, 700)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        self.scene = QGraphicsScene()
        self.view = QGraphicsView(self.scene)
        self.view.setRenderHint(QPainter.Antialiasing)

        self.layer_sequence = [
            layer.name
            for layer in self.cable.layers
        ]

        layer_layout = QHBoxLayout()

        self.layer_dropdown = QComboBox()
        self.layer_dropdown.addItems(self.layer_sequence)

        self.input_field = QLineEdit()
        self.update_placeholder(self.layer_dropdown.currentText())

        self.layer_dropdown.currentTextChanged.connect(
            self.update_placeholder
        )

        self.update_layer_button = QPushButton("Update Layer")

        layer_layout.addWidget(QLabel("Layer:"))
        layer_layout.addWidget(self.layer_dropdown)
        layer_layout.addWidget(QLabel("Value:"))
        layer_layout.addWidget(self.input_field)
        layer_layout.addWidget(self.update_layer_button)

        installation_layout = QHBoxLayout()

        self.spacing_input = QLineEdit(str(self.installation.spacing))
        self.spacing_input.setPlaceholderText("Spacing (mm)")

        self.depth_input = QLineEdit(str(self.installation.depth))
        self.depth_input.setPlaceholderText("Depth (mm)")

        self.update_installation_button = QPushButton(
            "Update Installation"
        )

        installation_layout.addWidget(QLabel("Spacing:"))
        installation_layout.addWidget(self.spacing_input)
        installation_layout.addWidget(QLabel("Depth:"))
        installation_layout.addWidget(self.depth_input)
        installation_layout.addWidget(self.update_installation_button)

        duct_bank_layout = QGridLayout()

        bank = self.installation.concrete_duct_bank

        self.bank_num_cables_input = QLineEdit(str(bank.num_cables))
        self.bank_num_cables_input.setPlaceholderText("Number of cables")

        self.bank_width_input = QLineEdit(str(bank.width))
        self.bank_width_input.setPlaceholderText("Short side")

        self.bank_height_input = QLineEdit(str(bank.height))
        self.bank_height_input.setPlaceholderText("Long side")

        self.bank_top_cover_input = QLineEdit(str(bank.top_cover))
        self.bank_top_cover_input.setPlaceholderText("Top cover (m)")

        self.bank_concrete_resistivity_input = QLineEdit(
            str(bank.concrete_resistivity)
        )
        self.bank_concrete_resistivity_input.setPlaceholderText(
            "Concrete resistivity"
        )

        self.bank_backfill_resistivity_input = QLineEdit(
            str(bank.backfill_resistivity)
        )
        self.bank_backfill_resistivity_input.setPlaceholderText(
            "Backfill resistivity"
        )

        self.update_duct_bank_button = QPushButton(
            "Update Duct Bank"
        )

        duct_bank_layout.addWidget(QLabel("No. Cables:"), 0, 0)
        duct_bank_layout.addWidget(self.bank_num_cables_input, 0, 1)
        duct_bank_layout.addWidget(QLabel("Short Side (m):"), 0, 2)
        duct_bank_layout.addWidget(self.bank_width_input, 0, 3)
        duct_bank_layout.addWidget(QLabel("Long Side (m):"), 0, 4)
        duct_bank_layout.addWidget(self.bank_height_input, 0, 5)

        duct_bank_layout.addWidget(QLabel("Top Cover (m):"), 1, 0)
        duct_bank_layout.addWidget(self.bank_top_cover_input, 1, 1)
        duct_bank_layout.addWidget(QLabel("Concrete rho:"), 1, 2)
        duct_bank_layout.addWidget(
            self.bank_concrete_resistivity_input,
            1,
            3
        )
        duct_bank_layout.addWidget(QLabel("Backfill rho:"), 1, 4)
        duct_bank_layout.addWidget(
            self.bank_backfill_resistivity_input,
            1,
            5
        )
        duct_bank_layout.addWidget(self.update_duct_bank_button, 1, 6)

        main_layout.addLayout(layer_layout)
        main_layout.addLayout(installation_layout)
        main_layout.addLayout(duct_bank_layout)
        main_layout.addWidget(self.view)

        self.ampacity_label = QLabel("Ampacity:")
        self.rac_label = QLabel("AC Resistance:")
        self.t1_label = QLabel("T1:")
        self.t4_label = QLabel("T4 Total:")

        main_layout.addWidget(self.ampacity_label)
        main_layout.addWidget(self.rac_label)
        main_layout.addWidget(self.t1_label)
        main_layout.addWidget(self.t4_label)

        self.setCentralWidget(central_widget)

        self.update_layer_button.clicked.connect(
            self.update_layer
        )

        self.update_installation_button.clicked.connect(
            self.update_installation
        )

        self.update_duct_bank_button.clicked.connect(
            self.update_duct_bank
        )

        self.draw_cable()
        self.recalculate()

    def update_layer(self):
        selected_layer = self.layer_dropdown.currentText()
        value_text = self.input_field.text()

        if not value_text:
            return

        try:
            value = float(value_text)
        except ValueError:
            return

        if value <= 0:
            return

        index = self.layer_sequence.index(selected_layer)

        self.cable.update_layer_value(index, value)

        self.recalculate()
        self.draw_cable()

        self.input_field.clear()

    def update_placeholder(self, selected_layer):
        index = self.layer_sequence.index(selected_layer)
        layer = self.cable.layers[index]

        if layer.is_base:
            self.input_field.setPlaceholderText("Diameter (mm)")
        else:
            self.input_field.setPlaceholderText("Thickness (mm)")

    def update_installation(self):
        spacing_text = self.spacing_input.text()
        depth_text = self.depth_input.text()

        if not spacing_text or not depth_text:
            return

        try:
            spacing = float(spacing_text)
            depth = float(depth_text)
        except ValueError:
            return

        if spacing <= 0 or depth <= 0:
            return

        self.installation.spacing = spacing
        self.installation.depth = depth

        self.recalculate()

    def update_duct_bank(self):
        bank = self.installation.concrete_duct_bank

        if bank is None:
            return

        try:
            num_cables = int(self.bank_num_cables_input.text())
            width = float(self.bank_width_input.text())
            height = float(self.bank_height_input.text())
            top_cover = float(self.bank_top_cover_input.text())
            concrete_resistivity = float(
                self.bank_concrete_resistivity_input.text()
            )
            backfill_resistivity = float(
                self.bank_backfill_resistivity_input.text()
            )

        except ValueError:
            return

        if (
            num_cables <= 0
            or width <= 0
            or height <= 0
            or top_cover <= 0
            or concrete_resistivity <= 0
            or backfill_resistivity <= 0
        ):
            return

        bank.num_cables = num_cables
        bank.width = width
        bank.height = height
        bank.top_cover = top_cover
        bank.concrete_resistivity = concrete_resistivity
        bank.backfill_resistivity = backfill_resistivity

        self.recalculate()

    def draw_cable(self):
        self.scene.clear()

        scale = 2.0
        minimum_visual_thickness = 1.2

        visual_radii = []
        previous_actual_radius = 0
        cumulative_visual_radius = 0

        for layer in self.cable.layers:
            actual_radius = layer.outer_radius

            if previous_actual_radius == 0:
                cumulative_visual_radius = actual_radius * scale
            else:
                actual_thickness = (
                    actual_radius - previous_actual_radius
                )

                visual_thickness = max(
                    actual_thickness * scale,
                    minimum_visual_thickness
                )

                cumulative_visual_radius += visual_thickness

            visual_radii.append(
                (
                    cumulative_visual_radius,
                    layer.color
                )
            )

            previous_actual_radius = actual_radius

        for radius, color in reversed(visual_radii):
            self.scene.addEllipse(
                -radius,
                -radius,
                2 * radius,
                2 * radius,
                QPen(QColor("#222222"), 0.5),
                QBrush(QColor(color))
            )

        self.view.fitInView(
            self.scene.itemsBoundingRect(),
            Qt.KeepAspectRatio
        )

    def recalculate(self):
        results = self.engine.calculate()

        self.ampacity_label.setText(
            f"Ampacity: {results.ampacity:.2f} A"
        )

        self.rac_label.setText(
            f"AC Resistance: "
            f"{results.electrical.ac_resistance:.5f} ohm/km"
        )

        self.t1_label.setText(
            f"T1: {results.thermal.T1:.3f}"
        )

        self.t4_label.setText(
            f"T4 Total: {results.thermal.T4_total:.3f}"
        )
