from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QGroupBox,
    QLabel,
    QMainWindow,
    QPushButton,
    QWidget,
    QVBoxLayout,
    QHBoxLayout,
    QFormLayout,
    QGraphicsScene,
    QGraphicsView,
    QComboBox,
    QLineEdit,
)

from PySide6.QtGui import (
    QPainter,
    QPen,
    QBrush,
    QColor,
)

from PySide6.QtCore import Qt

class MainWindow(QMainWindow):

    def __init__(self, cable, installation, environment, engine):
        super().__init__() # this tells the QmainWindow to create itself.

        self.cable = cable
        self.installation = installation
        self.environment = environment
        self.engine = engine


        self.setWindowTitle("IEC 60287 Cable Ampacity GUI")
        self.resize(1000,700)

        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)

        # ---------------------------------------
        # ---creating Cable drawing--------------
        # ---------------------------------------

        self.scene = QGraphicsScene() # for the cable drawing
        self.view = QGraphicsView(self.scene) # for viewing the cable drawing
        self.view.setRenderHint(QPainter.Antialiasing) # for better quality

        # ---------------------------------------
        # ---creating the duct bank drawing------
        # ---------------------------------------

        self.duct_bank_scene = QGraphicsScene() # for the duct bank drawing
        self.duct_bank_view = QGraphicsView(self.duct_bank_scene) # for viewing the duct bank drawing
        self.duct_bank_view.setRenderHint(QPainter.Antialiasing) # for better quality

        # ---------------------------------------
        # ----Drawings - To be managed ----------
        # ---------------------------------------



        # ----------------------------------------------------
        # -------Layer Layout. Module 02           -----------
        # will be created in the GUI main layout. ------------
        # It will show the layer sequence of the cable.-------
        # ----------------------------------------------------

        self.layer_sequence = [
            layer.name for layer in self.cable.layers # It will create a list of layer names in the order they are added to the cable
        ]

        cable_group = QGroupBox("Cable Layer Properties") # group box for the cable drawing
        layer_layout = QHBoxLayout() # horizontal layout for the layer sequence

        self.layer_dropdown = QComboBox() # select the cable layer to modify.
        self.layer_dropdown.addItems(self.layer_sequence) # adding the layer names to the dropdown

        self.input_field = QLineEdit() # for entering input values
        self.update_placeholder(self.layer_dropdown.currentText()) # setting the placeholder text for the input field

        self.layer_dropdown.currentTextChanged.connect(self.update_placeholder) # updating the placeholder text when the selected layer changes

        self.update_layer_button = QPushButton("Update Layer") # button to update the layer drawing

        layer_layout.addWidget(QLabel("Select Layer:")) # label for the dropdown
        layer_layout.addWidget(self.layer_dropdown) # adding the dropdown to the layout
        layer_layout.addWidget(QLabel("Input Value:")) # label for the input field
        layer_layout.addWidget(self.input_field) # adding the input field to the layout
        layer_layout.addWidget(self.update_layer_button) # adding the update button to the layout


        cable_group.setLayout(layer_layout) # setting the layout of the cable group box to the layer layout
        # -----------------------------------------------------
        # -------[Cable]Installation Layout. Module 03 --------
        # -----------------------------------------------------
        installation_group = QGroupBox("Cable Installation Parameters") # group box for the installation parameters
        installation_layout = QHBoxLayout() # horizontal layout for the installation parameters

        self.spacing_input = QLineEdit(str(self.installation.spacing)) # input field for spacing
        self.spacing_input.setPlaceholderText("Spacing (mm)") # setting the placeholder text for the spacing input field

        self.depth_input = QLineEdit(str(self.installation.depth)) # input field for depth
        self.depth_input.setPlaceholderText("Depth (mm)") # setting the placeholder text for the depth input field

        self.update_installation_button = QPushButton("Update Installation") # button to update the installation parameters

        installation_layout.addWidget(QLabel("Spacing (mm):")) # label for spacing
        installation_layout.addWidget(self.spacing_input) # adding the spacing input field to the layout
        installation_layout.addWidget(QLabel("Depth (mm):")) # label for depth
        installation_layout.addWidget(self.depth_input) # adding the depth input field to the layout
        installation_layout.addWidget(self.update_installation_button) # adding the update button to the layout

        installation_group.setLayout(installation_layout) # setting the layout of the installation group box to the installation layout

        # ----------------------------------------------------
        # -------Duct Bank Layout[Concrete]. Module 04--------
        # ----------------------------------------------------
        duct_bank_group = QGroupBox("Concrete Duct Bank Parameters") # group box for the duct bank parameters
        duct_bank_layout = QGridLayout() # grid layout for the duct bank 
        
        bank = self.installation.concrete_duct_bank # getting the concrete duct bank object from the installation object

        self.bank_num_cables_input = QLineEdit(str(bank.num_cables)) # input field for number of cables
        self.bank_num_cables_input.setPlaceholderText("Number of Cables") # setting the placeholder text for the number of cables input field

        self.bank_width_input = QLineEdit(str(bank.width)) # input field for shorter side of the duct bank
        self.bank_width_input.setPlaceholderText("shorter side of the duct bank (m)") # setting the placeholder text

        self.bank_height_input = QLineEdit(str(bank.height)) # input field for longer side of the duct bank
        self.bank_height_input.setPlaceholderText("longer side of the duct bank (m)") # setting the placeholder text

        self.bank_top_cover_input = QLineEdit(str(bank.top_cover)) # input field for top cover
        self.bank_top_cover_input.setPlaceholderText("Top Cover (m)") # setting the placeholder text

        self.bank_concrete_resistivity_input = QLineEdit(str(bank.concrete_resistivity)) # input field for concrete resistivity
        self.bank_concrete_resistivity_input.setPlaceholderText("Concrete Resistivity (ohm.m)") # setting the placeholder text

        self.bank_backfill_resistivity_input = QLineEdit(str(bank.backfill_resistivity)) # input field for backfill resistivity
        self.bank_backfill_resistivity_input.setPlaceholderText("Backfill Resistivity (ohm.m)") # setting the placeholder text 

        self.update_duct_bank_button = QPushButton("Update Duct Bank") # button to update the duct bank parameters  

        duct_bank_layout.addWidget(QLabel("Number of Cables:"), 0, 0) # label for number of cables
        duct_bank_layout.addWidget(self.bank_num_cables_input, 0, 1) # adding the number of cables input field to the layout

        duct_bank_layout.addWidget(QLabel("Shorter Side (m):"), 1, 0) # label for shorter side
        duct_bank_layout.addWidget(self.bank_width_input, 1, 1) # adding the shorter side input field to the layout

        duct_bank_layout.addWidget(QLabel("Longer Side (m):"), 1, 2) # label for longer side
        duct_bank_layout.addWidget(self.bank_height_input, 1, 3) # adding the longer side input field to the layout

        duct_bank_layout.addWidget(QLabel("Top Cover (m):"), 1, 4) # label for top cover
        duct_bank_layout.addWidget(self.bank_top_cover_input, 1, 5) # adding the top cover input field to the layout

        duct_bank_layout.addWidget(QLabel("Concrete Resistivity (ohm.m):"), 0, 2) # label for concrete resistivity
        duct_bank_layout.addWidget(self.bank_concrete_resistivity_input, 0, 3) # adding the concrete resistivity input field to the layout

        duct_bank_layout.addWidget(QLabel("Backfill Resistivity (ohm.m):"), 0, 4) # label for backfill resistivity
        duct_bank_layout.addWidget(self.bank_backfill_resistivity_input, 0, 5) # adding the backfill resistivity input field to the layout

        duct_bank_layout.addWidget(self.update_duct_bank_button, 2, 2, 1, 2) # adding the update button to the layout 



        duct_bank_group.setLayout(duct_bank_layout) # setting the layout of the duct bank group box to the duct bank layout


        # ----------------------------------------------------
        # ------DRAWINGS LAYOUTS [Cable and Duct Bank]--------
        # -------------MODULE 05------------------------------


        drawings_group = QGroupBox("Drawings") # group box for the drawings
        drawings_layout = QHBoxLayout() # horizontal layout for the drawings

        drawings_layout.addWidget(self.view) # adding the cable drawing view to the layout
        drawings_layout.addWidget(self.duct_bank_view) # adding the duct bank drawing view to the layout

        drawings_group.setLayout(drawings_layout) # setting the layout of the drawings group box to the drawings layout

        # -----------------------------------------------------
        # ------Results Layout [Module 06]---------------------
        # -----------------------------------------------------

        results_group = QGroupBox("Results")
        results_layout = QHBoxLayout() # this is the layout where we will nest our
                                        # 1. Ampacity group
                                        # 2. Electrical group
                                        # 3. Thermal group

        # 1. ********Ampacity group**********
        overall_group = QGroupBox("OverAll")
        overall_layout = QFormLayout()

        self.ampacity_value = QLabel("--A")

        overall_layout.addRow("Ampacity of Cable:",self.ampacity_value) # add row to the form

        overall_group.setLayout(overall_layout)

        # 2. **********Electrical group *************
        electrical_group = QGroupBox("Electrical")
        electrical_layout = QFormLayout()

        self.rdc_value = QLabel("-- Ω/km")
        self.rac_value = QLabel("-- Ω/km")
        self.skin_effect_value = QLabel("--")
        self.proximity_effect_value = QLabel("--")

        electrical_layout.addRow("DC Resistance:", self.rdc_value)
        electrical_layout.addRow("AC Resistance:", self.rac_value)
        electrical_layout.addRow("Skin Effect (Ys):", self.skin_effect_value)
        electrical_layout.addRow("Proximity Effect (Yp):", self.proximity_effect_value)

        electrical_group.setLayout(electrical_layout)

        # 3. ********Thermal********************
        thermal_group = QGroupBox("Thermal")
        thermal_layout = QFormLayout()

        self.t1_value = QLabel("--")
        self.t2_value = QLabel("--")
        self.t3_value = QLabel("--")
        self.t4_duct_value = QLabel("--")
        self.t4_total_value = QLabel("--")

        thermal_layout.addRow("T1:", self.t1_value)
        thermal_layout.addRow("T2:", self.t2_value)
        thermal_layout.addRow("T3:", self.t3_value)
        thermal_layout.addRow("T4 Duct:", self.t4_duct_value)
        thermal_layout.addRow("T4 Total:", self.t4_total_value)

        thermal_group.setLayout(thermal_layout)


        # *****Assemble everything in results Layout *****

        results_layout.addWidget(overall_group)
        results_layout.addWidget(electrical_group)
        results_layout.addWidget(thermal_group)

        results_group.setLayout(results_layout)




        # ----------------------------------------------------#
        # --Adding the layouts to the main layout of the GUI--#
        # ----------------------------------------------------#
        
        main_layout.addWidget(cable_group) # adding the cable group box to the main layout
        main_layout.addWidget(installation_group) # adding the installation group box to the main layout
        main_layout.addWidget(duct_bank_group) # adding the duct bank group box to the main layout
        main_layout.addWidget(drawings_group) # adding the drawings group box to the main layout
        main_layout.addWidget(results_group) # adding the results group


        self.setCentralWidget(central_widget) # setting the central widget of the main window to the central widget we created

        # ----------------------------------------------------
        # -------Connecting the buttons to their functions----
        # ----------------------------------------------------

        self.update_layer_button.clicked.connect(self.update_layer) # connecting the update layer button[Module 02] to the update_layer function
        self.update_installation_button.clicked.connect(self.update_installation) # connecting the update installation button[Module 03] to the update_installation function
        self.update_duct_bank_button.clicked.connect(self.update_duct_bank) # connecting the update duct bank button[Module 04] to the update_duct_bank function

        # ----------------------------------------------------
        # -------Initial Drawing of Cable and Duct Bank--------
        # ----------------------------------------------------
        self.draw_cable() # initial drawing of the cable
        self.draw_duct_bank() # initial drawing of the duct bank
        self.recalculate() # call the function to display the results 



        # ----------------------------------------------------
        # ------------Function Definitions for GUI Actions----
        # ----------------------------------------------------
        # --Later to be added to MainController class for ----
        # --better structure and separation of concerns-------
        # ----------------------------------------------------

    def update_placeholder(self, selected_layer = None):
        index = self.layer_sequence.index(selected_layer)
        layer = self.cable.layers[index]

        if layer.is_base:
            self.input_field.setPlaceholderText("Diameter (mm)")
        else:
            self.input_field.setPlaceholderText("Thickness (mm)")

    def update_layer(self): # For Cable Layer Properties. Module 02
        selected_layer = self.layer_dropdown.currentText()
        index = self.layer_sequence.index(selected_layer)
        value_text = self.input_field.text()
        
        if not value_text:
            print("Input field is empty. Please enter a value.")
            return

        try:
            value = float(self.input_field.text())
        except ValueError:
            print("Invalid input. Please enter a numeric value.")
            return
        
        if value <= 0:
            print("Invalid input. Please enter a positive value.")
            return 
        
        self.cable.update_layer_value(index, value) # updating the layer value in the cable object

        self.recalculate() # recalculate the cable properties after updating the layer
        self.draw_cable() # redraw the cable after updating the layer
        self.draw_duct_bank() # redraw the duct bank after updating the layer

        self.input_field.clear() # clear the input field after updating the layer.

    def update_installation(self): # For Cable Installation Parameters. Module 03
        spacing_text = self.spacing_input.text()
        depth_text = self.depth_input.text()

        if not spacing_text or not depth_text:
            print("Input fields are empty. Please enter values.")
            return
        
        try:
            spacing = float(spacing_text)
            depth = float(depth_text)

        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return
        
        if spacing <= 0 or depth <= 0:
            print("Invalid input. Please enter positive values.")
            return
        
        self.installation.spacing = spacing
        self.installation.depth = depth

        self.recalculate() # recalculate the cable properties after updating the installation parameters
        self.draw_duct_bank() # redraw the duct bank after updating the installation parameters.

    def update_duct_bank(self): # For Concrete Duct Bank Parameters. Module 04
        bank = self.installation.concrete_duct_bank

        try:
            num_cables = int(self.bank_num_cables_input.text())
            width = float(self.bank_width_input.text())
            height = float(self.bank_height_input.text())
            top_cover = float(self.bank_top_cover_input.text())
            concrete_resistivity = float(self.bank_concrete_resistivity_input.text())
            backfill_resistivity = float(self.bank_backfill_resistivity_input.text())

        except ValueError:
            print("Invalid input. Please enter numeric values.")
            return
        
        if num_cables <= 0 or width <= 0 or height <= 0 or top_cover <= 0 or concrete_resistivity <= 0 or backfill_resistivity <= 0:
            print("Invalid input. Please enter positive values.")
            return
        
        bank.num_cables = num_cables
        bank.width = width
        bank.height = height
        bank.top_cover = top_cover
        bank.concrete_resistivity = concrete_resistivity
        bank.backfill_resistivity = backfill_resistivity

        self.recalculate() # recalculate the cable properties after updating the duct bank parameters
        self.draw_duct_bank() # redraw the duct bank after updating the duct bank parameters.
        


    def recalculate(self):
        # ------------------------------------------
        # -Recalculate the IEC 60287 engineering model.
        # -------------------------------------------

        self.results = self.engine.calculate()

        self.update_results() # Call update results function

    def draw_cable(self):
        self.scene.clear() # clear the previous drawing

        scale = 2.0 # scale factor for the drawing
        minimum_visual_thickness = 1.2 # minimum thickness for visual representation

        visual_radii = [] # list to store the visual radii of the layers for drawing
        previous_actual_radius = 0.0 # variable to store the previous actual radius for calculating the visual radius   
        cumulative_visual_radius = 0.0 # variable to store the cumulative visual radius for drawing

        for layer in self.cable.layers:
            actual_radius = layer.outer_radius # getting the actual outer radius of the layer

            if previous_actual_radius == 0.0:
                cumulative_visual_radius = actual_radius * scale # for the first layer, the visual radius is the actual radius scaled

            else:
                actual_thickness = actual_radius - previous_actual_radius # calculating the actual thickness of the layer
                visual_thickness = max(actual_thickness * scale, minimum_visual_thickness) # calculating the visual thickness of the layer
                
                cumulative_visual_radius += visual_thickness # updating the cumulative visual radius for drawing

            visual_radii.append((cumulative_visual_radius,layer.color)) # adding the cumulative visual radius to the list for drawing
            previous_actual_radius = actual_radius # updating the previous actual radius for the next iteration

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


    def draw_duct_bank(self):
        self.duct_bank_scene.clear() # clear the previous drawing

        bank = self.installation.concrete_duct_bank # getting the concrete duct bank object from the installation object
        duct = self.installation.duct # getting the duct object from the installation object

        if bank is None or duct is None:
            self.duct_bank_scene.addText("No duct bank data")
            return
        
        scale = 320 # scale factor for the drawing, adjusted for better visibility

        bank_width = bank.height * scale # converting the bank width to pixels for drawing
        bank_height = bank.width * scale # converting the bank height to pixels for drawing
        top_cover = bank.top_cover * scale # converting the top cover to pixels for drawing 

        spacing = self.installation.spacing * scale / 1000 # converting the spacing to pixels for drawing

        duct_outer_diameter = duct.outer_diameter * scale / 1000 # converting the duct outer diameter to pixels for drawing
        duct_inner_diameter = duct.inner_diameter * scale / 1000 # converting the duct inner diameter to pixels for drawing

        cable_diameter = self.cable.layers[-1].diameter * scale

        # defining the bounding rectangle for the duct bank
        bank_left = -bank_width / 2
        bank_top = 0

        concrete_pen = QPen(QColor("#555555"), 1.5)
        concrete_brush = QBrush(QColor("#d8d8d8"))

        self.duct_bank_scene.addRect( # drawing the concrete duct bank
            bank_left,
            bank_top,
            bank_width,
            bank_height,
            concrete_pen, # pen for the concrete duct bank, draws the outline of the rectangle
            concrete_brush # brush for the concrete duct bank, fills the rectangle with the specified color
        )        

        # now adding the top cover above the duct bank
        ground_y = -top_cover

        self.duct_bank_scene.addLine(
            bank_left - 60, # -60 pixels to the left of the duct bank
            ground_y, # y-coordinate of the ground line
            bank_left + bank_width + 60, # 60 pixels to the right of the duct bank
            ground_y, # y-coordinate of the ground line
            QPen(QColor("#6b4f2a"), 2)
        )

        # adding the text "Ground level" above the ground line
        self.duct_bank_scene.addText("Ground level").setPos(
            bank_left,
            ground_y - 25
        )

        # now calculating and positioning the number of cables with spacing in the duct bank
        count = bank.num_cables
        start_x = -((count - 1) * spacing) / 2 # starting x-coordinate for the first cable, centered in the duct bank
        center_y = bank_top + bank_height / 2  # we have to make it exactly like the case study.

        # now adding the ducts and cables in the duct bank

        phase_colors = [ # defining the colors for the phases of the cables
                         # later to be transferrd to the constants file.
                        "#FF0000",   # Red
                        "#FFFF00",   # Yellow
                        "#0000FF",   # Blue
                    ]
        for index in range(count):
            center_x = start_x + index * spacing # calculating the x-coordinate for each cable based on the index and spacing

            cable_color = phase_colors[index % len(phase_colors)]

            self.duct_bank_scene.addEllipse( # drawing the duct outer diameter
                center_x - duct_outer_diameter / 2,
                center_y - duct_outer_diameter / 2,
                duct_outer_diameter,
                duct_outer_diameter,
                QPen(QColor("#333333"), 1.2),
                QBrush(QColor("#b8c7d9"))
            )

            self.duct_bank_scene.addEllipse( # drawing the duct inner diameter
                center_x - duct_inner_diameter / 2,
                center_y - duct_inner_diameter / 2,
                duct_inner_diameter,
                duct_inner_diameter,
                QPen(QColor("#444444"), 0.8),
                QBrush(QColor("#f4f4f4"))
            )

            self.duct_bank_scene.addEllipse( # drawing the cable diameter
                center_x - cable_diameter / 2,
                center_y - cable_diameter / 2,
                cable_diameter,
                cable_diameter,
                QPen(QColor("#111111"), 0.8),
                QBrush(QColor(cable_color))
            )

        # ----------------------------------------------------
        # -------Duct Bank Dimensions. Longer side-----------
        # -------Draw Engineering Dimensions and Labels-------
        # ---------------------------------------------------

        dimension_pen = QPen(QColor("#1f4e79"), 1)

        bottom_y = bank_top + bank_height + 35
        self.duct_bank_scene.addLine(
            bank_left,
            bottom_y,
            bank_left + bank_width,
            bottom_y,
            dimension_pen
        )
        self.duct_bank_scene.addText(
            f"Long side = {bank.height:.3f} m"
        ).setPos(
            bank_left + bank_width / 2 - 70,
            bottom_y + 5
        )

        # -------------------------------------------------
        # ---- Shorter Side of the duct bank dimension and label
        # -------------------------------------------------

        right_x = bank_left + bank_width + 35
        self.duct_bank_scene.addLine(
            right_x,
            bank_top,
            right_x,
            bank_top + bank_height,
            dimension_pen
        )
        self.duct_bank_scene.addText(
            f"Short side = {bank.width:.3f} m"
        ).setPos(
            right_x + 5,
            bank_top + bank_height / 2 - 10
        )

       # -------------------------------------------------
       # ---Top Cover of the duct bank dimension and label
       # -------------------------------------------------
        cover_x = bank_left - 35
        self.duct_bank_scene.addLine(
            cover_x,
            ground_y,
            cover_x,
            bank_top,
            dimension_pen
        )
        self.duct_bank_scene.addText(
            f"Top cover = {bank.top_cover:.3f} m"
        ).setPos(
            cover_x - 95, # shifts the text to the left of the line
            (ground_y + bank_top) / 2 - 10
        )

        if count > 1: # if there is more than one cable, we will show the spacing between the cables
            self.duct_bank_scene.addText(
                f"Spacing = {self.installation.spacing:.0f} mm"
            ).setPos(
                -70,
                center_y + duct_outer_diameter / 2 + 10
            )

        # -------------------------------------------------
        # ---Duct and Cable Dimensions and Labels---------- 
        # ------------------------------------------------ 


        base_y = bank_top + bank_height + 70 # base y-coordinate for the labels below the duct bank
        line_spacing = 20 # vertical spacing between the labels
        self.duct_bank_scene.addText( # adding the duct outer and inner diameter label
            f"Duct OD/ID = {duct.outer_diameter:.0f}/{duct.inner_diameter:.0f} mm"
        ).setPos(
            bank_left,
            base_y
        )

        self.duct_bank_scene.addText( # adding the duct material label
            f"Duct Material = {duct.material}"
        ).setPos(
            bank_left,
            base_y + line_spacing
        )

        self.duct_bank_scene.addText( # adding the cable outer diameter label
            f"Cable OD = {self.cable.layers[-1].diameter * 1000:.1f} mm"
        ).setPos(
            bank_left,
            base_y + 2 * line_spacing
        )

        self.duct_bank_scene.addText( # adding the depth to group center label
            f"Depth to group center = {self.installation.depth:.0f} mm"
        ).setPos(
            bank_left,
            base_y + 3 * line_spacing
        )

        # -------------------------------------------------
        # ----better view of the duct bank drawing in the view
        # -------------------------------------------------
        self.duct_bank_view.fitInView(
            self.duct_bank_scene.itemsBoundingRect(),
            Qt.KeepAspectRatio
        )

    def update_results(self):
        """
        Update the Results panel with the latest IEC 60287 calculations.
        """

        if not hasattr(self, "results"):
            return

        electrical = self.results.electrical
        thermal = self.results.thermal

        # -------------------------------
        # Overall Results
        # -------------------------------
        self.ampacity_value.setText(
            f"{self.results.ampacity:.2f} A"
        )

        # -------------------------------
        # Electrical Results
        # -------------------------------
        self.rdc_value.setText(
            f"{electrical.dc_resistance:.5f} Ω/km"
        )

        self.rac_value.setText(
            f"{electrical.ac_resistance:.5f} Ω/km"
        )

        self.skin_effect_value.setText(
            f"{electrical.skin_effect:.5f}"
        )

        self.proximity_effect_value.setText(
            f"{electrical.proximity_effect:.5f}"
        )

    # -------------------------------
    # Thermal Results
    # -------------------------------
        self.t1_value.setText(
            f"{thermal.T1:.3f}"
        )

        self.t2_value.setText(
            f"{thermal.T2:.3f}"
        )

        self.t3_value.setText(
            f"{thermal.T3:.3f}"
        )

        self.t4_duct_value.setText(
            f"{thermal.T4_duct:.3f}"
        )

        self.t4_total_value.setText(
            f"{thermal.T4_total:.3f}"
        )








        
