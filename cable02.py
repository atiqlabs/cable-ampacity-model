from iec_constants import *


class Material:
     def __init__(self,name,thermal_resistivity=None,resistivity_20=None,temp_coefficient=None): # here you can add material properties later
          self.name = name # name of the material used like Cu, Al, xlpe etc not the names of layers 
          self.thermal_resistivity = thermal_resistivity
          self.resistivity_20 = resistivity_20 #Ohm.meter
          self.temp_coefficient = temp_coefficient

class CableLayer:
     def __init__(self,name,value,material,color,is_base = False, layer_type = None):
          self.name=name
          self.value = value # Diameter for base, thickness for others
          self.material=material
          self.color=color
          self.is_base = is_base # flag to identify conductor
          self.layer_type = layer_type # it will store type of layer like conductor, insulation , jacket aligning with SEC/IEC standards.
          self.diameter = None  # At 1st it has no value but after it updated check layer.diameter in _recalculate_geometry
                                # self.diameter would store value that would be used in ampacity calculations.

     @property
     def outer_radius(self):
          return self.diameter/2 if self.diameter else 0

class Cable: # Cable Class
    """
    MV/HV Cable Constrction 
    Units: mm 
    """
    def __init__(self,cable_type,size,voltage,standard,
                 conductor_type ="Round/Milliken",
                 conductor_insulation_system ="Fluid/Paper/PPL"
                 ):
     # *******************START OF CABLE CONSTRUCTOR*****************

     # ----------------------------------------
     # ----CONDUCTOR BASIC INFO --------------
     #----------------------------------------

        self.cable_type = cable_type # taken from user
        self.size = size # taken from user
        self.voltage = voltage # taken from user
        self.standard = standard # taken from user


     # MATERIALS
        self.materials = self._create_materials()

     # MAP INPUTS
        self.conductor_type = self._map_conductor_type(conductor_type) # taken from user
        self.conductor_insulation_system = self._map_insulation_system(conductor_insulation_system) # taken from user
     
     # LAYERS
        self.layers = [] #initiate array
        self.create_default_layer() # auto create layers

     #When Using and assigning internal functions It can be done like this. Note the use of "_" before function"""
     # -----------------------------------
     # -----MATERIAL SETUP----------------
     #----------------------------------- 
     
     # Define Materials of the layers and their properties here ********** Table 01 IEC 60287-2-1

    def _create_materials(self): 
          return {
              "Copper" : Material("Copper",**COPPER), # ** Take values in exactly the same manner as defined in iec_constants.py
              "XLPE" : Material("XLPE",**XLPE),
              "Semiconductor" : Material("Semiconductor",**SEMICONDUCTOR), # confirm, the semiconducting materials have the same thermal properties as the adjacent dielectric materials, Ref Table 01 IEC 60287-2-1:2023
              "HDPE" : Material("HDPE",**HDPE), # confirm the thermal resistivity
              "Aluminium" : Material("Aluminium",**ALUMINIUM),
              "Graphite" : Material("Graphite",**GRAPHITE) # from others in table

          }
    
     # -----------------------------------
     # -----MAPPING FUNCTIONS-------------
     #-----------------------------------
    def _map_conductor_type(self, conductor_type):
         mapping = {
              "Round/Milliken": "milliken",
              "Round/Solid": "solid"
         }

         if conductor_type not in mapping:
              raise ValueError(f"Invalid conductor type: {conductor_type}")
         
         return mapping[conductor_type]
    def _map_insulation_system(self, insulation):
         mapping = {
              "Fluid/Paper/PPL": "paper"
         }

         if insulation not in mapping:
              raise ValueError(f"Invalid insulation system: {insulation}")
         
         return mapping[insulation]
     


        # ***************** END of Cable Constructor ******************


     #--------------------------------------
     # ------Layer Creation-----------------
     # -------------------------------------   

    def create_default_layer(self):
          default_layers = [
        ("Sealed Conductor", 43,"Copper", "#b87333", True, "conductor"),
        ("SCWB Tape 1", 0.5,"Semiconductor", "#d3d3d3", False, "semiconductor"),
        ("Inner Semi", 2,"Semiconductor", "red", False, "semiconductor"),
        ("XLPE", 18,"XLPE", "#0000CD", False, "insulation"),
        ("Outer Semi", 1.5,"Semiconductor", "gray", False, "semiconductor"),
        ("SCWB Tape 2", 0.5,"Semiconductor", "#d3d3d3", False, "semiconductor"),
        ("Cu Screen", 2,"Copper", "brown", False, "screen"),
        ("SCWB Tape 3", 0.5,"Semiconductor", "#d3d3d3", False, "semiconductor"),
        ("Al Tape", 0.5,"Aluminium", "#A9ACB6", False, "sheath"),
        ("HDPE Jacket", 4.5,"HDPE", "black", False, "jacket"),
        ("Graphite", 0.9,"Graphite", "#778899", False, "outer_layer"),
          ]

          for name,value,material_name,color,is_base,layer_type in default_layers:
               material = self.materials[material_name] # looks for dictionary
               self.add_layer(name,value,material,color,is_base,layer_type)


     #-------------------------------------
     #---------PUBLIC METHODS--------------
     #------------------------------------

    def add_layer(self,name, value, material,color,is_base = False, layer_type = None): # "value" is diameter for conductor while thickness for other layers
         layer = CableLayer(name,value,material,color,is_base, layer_type)
         self.layers.append(layer)
         self._recalculate_geometry()

    def update_layer_value(self,index,new_value): # this is a slight modification and update for GUI 
         self.layers[index].value = new_value
         self._recalculate_geometry()

     # ------------------------------
     #----GEOMETRY CALCULATIONS------
     #-------------------------------

    def _recalculate_geometry(self):
         current_diameter = 0

         for layer in self.layers:
              if layer.is_base:
                   current_diameter = layer.value # stores conductor diameter if flag is true
              else:
                   current_diameter += 2*layer.value
         
              layer.diameter = current_diameter




