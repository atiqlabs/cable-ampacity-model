import math

# ---------- Electrical ----------
COPPER = {
    "resistivity_20": 1.724e-8,
    "temp_coefficient": 0.00393
}

ALUMINIUM = {
    "resistivity_20": 2.826e-8,
    "temp_coefficient": 0.00403
}

# ---------- Thermal ----------
XLPE = {
    "thermal_resistivity": 3.5
}

HDPE = {
    "thermal_resistivity": 3.5 # taken from Riyadh Cables Calculations
}

SEMICONDUCTOR = {
    "thermal_resistivity": 2.5 # from Jeddah cables Data schedule and also Table 01 of IEC 60287-2-1
}

GRAPHITE = {
    "thermal_resistivity": 5.0
}

# ---------- General ----------
MU_0 = 4 * math.pi * 1e-7
DEFAULT_FREQUENCY = 60


# Using Table 02 of IEC60287-1-1-2023 for kp and ks, for now i am adding some values in future we have to upgrade it to full table according to the types of cable input from user.
IEC_CONDUCTOR_TABLE02 = {
    ("Copper","solid","All"):{ # use simple names, howver, they are mapped in the cable.init in cable02 file, once you get input from user
        "ks":1,
        "kp":1
    },
    ("Copper","milliken","paper"):{
        "ks":0.435,
        "kp":0.37
    }

    # in future extend here the table
}

# -----------Temperature Modes according to NG Standards --------------
OPERATING_TEMPERATURES = {
    "normal":90,
    "emergency":105,
    "fault":250
}

#------------------------------------------------
# ---------- DUCTS MATERIALS PROPERTIES ---------
#------------------------------------------------

DUCT_MATERIALS = {
    "PVC": {"thermal_resistivity": 6},
    "HDPE": {"thermal_resistivity": 5},
    "CONCRETE":{"thermal_resistivity":1.2}
}
    