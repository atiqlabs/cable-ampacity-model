
from PySide6.QtWidgets import (QMainWindow, QGraphicsScene, QGraphicsView,QComboBox,QLineEdit,QPushButton,QLabel,QHBoxLayout )
from PySide6.QtGui import QBrush, QPen , QColor
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout
from src.models.cable import Material, Cable

class MainWindow(QMainWindow):
    def __init__(self,cable):
        super().__init__() # takes all properties of QMainwindow
        self.cable = cable
        self.setWindowTitle("Cable GUI")
        self.resize(800,600)
        central_widget = QWidget() # create an empty widget
        main_layout = QVBoxLayout(central_widget) # creates main layout vertically

        # create Scene and view
        self.scene = QGraphicsScene() # creates the scenes e.g draw the cable in scenes
        self.view = QGraphicsView(self.scene) # it shows the scenes


        ## new ##
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

        """self.layer_colors = {
        "Sealed Conductor": "#b87333",   # copper brown
        "SCWB Tape 1": "#d3d3d3",        # light gray
        "Inner Semi": "red",
        "XLPE": "#0000CD",               # blue
        "Outer Semi": "gray",
        "SCWB Tape 2": "#d3d3d3",
        "Cu Screen": "brown",
        "SCWB Tape 3": "#d3d3d3",
        "Al Tape": "#A9ACB6",
        "HDPE Jacket": "black",
        "Graphite": "#778899"
        }"""

        # Control #
        control_layout = QHBoxLayout() # control layout is created in horizental position

        self.layer_dropdown = QComboBox() # creates combo box
        self.layer_dropdown.addItems(self.layer_sequence) # add list to the combo box

        self.input_field = QLineEdit() # create input field

        self.update_placeholder(self.layer_dropdown.currentText())
        self.layer_dropdown.currentTextChanged.connect(self.update_placeholder) # this line decides for place holder
        #self.input_field.setPlaceholderText("Diameter(mm)") # placeholder inside the line, It was very simple

        self.add_button = QPushButton("Update Layer") # add push button

        # Populate the control layout 
        control_layout.addWidget(QLabel("Layer:")) # 
        control_layout.addWidget(self.layer_dropdown)
        control_layout.addWidget(QLabel("Value:")) # add label to the input field
        control_layout.addWidget(self.input_field)
        control_layout.addWidget(self.add_button)

        # Add layouts
        main_layout.addLayout(control_layout) # add control layout to mainlayout
        main_layout.addWidget(self.view) # add view scene to the main layout

        self.setCentralWidget(central_widget)
        self.add_button.clicked.connect(self.add_layer)

        
        
        self.draw_cable()
        
    def add_layer(self):

        selected_layer = self.layer_dropdown.currentText()
        value_text = self.input_field.text()

        if not value_text:
            return
        try:
             value = float(value_text)
        except ValueError:
            return

        # Find index of selected layer
        index = self.layer_sequence.index(selected_layer)


        # Update backend layer value
        self.cable.update_layer_value(index, value)

        # Redraw
        self.draw_cable()

        self.input_field.clear()

    def update_placeholder(self,selected_layer):
        index = self.layer_sequence.index(selected_layer)

        layer = self.cable.layers[index]

        if layer.is_base:
            self.input_field.setPlaceholderText("Diameter (mm)")
        else:
            self.input_field.setPlaceholderText("Thickness (mm)")



    def draw_cable(self):
        self.scene.clear()

        for layer in reversed(self.cable.layers): # draws layers from reversed order. only nazar ka dhoka
            r = layer.outer_radius
            self.scene.addEllipse(
                -r, -r, 2*r, 2*r,
                QPen(Qt.black),
                QBrush(QColor(layer.color))
            )

        print("After Update")
        
        # just for debugging
        """for layer in self.cable.layers:
            print(f"Layer Name: {layer.name}, thickness: {layer.value},Dia: {layer.diameter}")"""


        #self.view.fitInView(self.scene.itemsBoundingRect(),Qt.KeepAspectRatio)
            # Auto scale view properly
        
        """self.view.fitInView(
            self.scene.itemsBoundingRect(),
            Qt.KeepAspectRatio
        )"""
