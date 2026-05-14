"""
Structured engineering result objects for IEC 60287 ampacity studies.

These classes define the output interface of the ampacity engine.

The purpose of these result models is to:
    - organize calculation outputs
    - provide stable access to engineering results
    - simplify GUI integration
    - simplify report generation
    - avoid fragile dictionary-based access

Result hierarchy:

AmpacityResults
│
├── ElectricalResults
├── ThermalResults
└── ampacity
"""


class ElectricalResults:
    """
    Stores electrical calculation results according to IEC 60287.

    Includes:
        - DC conductor resistance
        - skin effect factor
        - proximity effect factor
        - AC resistance
    """

    def __init__(
        self,
        dc_resistance,
        skin_effect,
        proximity_effect,
        ac_resistance
    ):

        self.dc_resistance = dc_resistance
        self.skin_effect = skin_effect
        self.proximity_effect = proximity_effect
        self.ac_resistance = ac_resistance


class ThermalResults:
    """
    Stores thermal resistance results according to IEC 60287.

    Includes:
        - T1 : conductor to sheath
        - T2 : sheath to armour
        - T3 : outer jacket
        - T4_duct : duct thermal resistance
        - T4_total : total external thermal resistance
    """

    def __init__(
        self,
        T1,
        T2,
        T3,
        T4_duct,
        T4_total
    ):

        self.T1 = T1
        self.T2 = T2
        self.T3 = T3
        self.T4_duct = T4_duct
        self.T4_total = T4_total


class AmpacityResults:
    """
    High-level IEC 60287 ampacity study results.

    Combines:
        - electrical results
        - thermal results
        - final ampacity

    This object represents the complete output of an
    ampacity calculation study.
    """

    def __init__(
        self,
        electrical,
        thermal,
        ampacity
    ):

        self.electrical = electrical
        self.thermal = thermal
        self.ampacity = ampacity