# Cable Ampacity Model (IEC 60287)

## 📌 Overview

This project implements a steady-state cable ampacity calculation based on IEC 60287 methodology.
It models both electrical losses and thermal resistances to compute allowable current under specified installation conditions.

---

## ⚡ Methodology

The ampacity is calculated using:

I = sqrt(Δθ / (R_ac × T_total))

Where:

* Δθ → temperature difference (conductor – ambient)
* R_ac → AC resistance of conductor (Ω/m)
* T_total → total thermal resistance (K·m/W)

---

## 🔧 Model Components

### Electrical Model

* DC resistance (temperature corrected)
* Skin effect (ys)
* Proximity effect (yp)
* AC resistance:
  R_ac = R_dc × (1 + ys + yp)

---

### Thermal Model

Total thermal resistance:

T_total = T1 + T2 + T3 + T4

#### Internal Resistances

* T1 → conductor to sheath
* T2 → sheath to armor (0 in this case)
* T3 → outer sheath

#### External Resistance (T4)

For **concrete duct bank installation**, T4 is decomposed as:

T4 = T′4 + T″4 + T‴4 + T⁗4

Where:

* T′4 → air gap between cable and duct
* T″4 → duct material resistance
* T‴4 → external thermal resistance of duct (concrete region)
* T⁗4 → correction factor (backfill ↔ concrete)

---

## 📊 Reference Case (Validated)

This implementation is validated against a real engineering calculation:

* Cable: 1 × 1200 mm² Cu XLPE (110 kV)
* Installation: Concrete duct bank
* Formation: Flat
* Spacing: 400 mm
* Depth: 1450 mm
* Duct: 200 / 225 mm (inner / outer)
* Soil resistivity: 1.2 K·m/W
* Conductor temperature: 90°C
* Ambient temperature: 40°C

### Results

| Parameter     | Value        |
| ------------- | ------------ |
| AC Resistance | 0.01952 Ω/km |
| T1            | 0.378        |
| T3            | 0.051        |
| T4            | ~3.10        |
| Ampacity      | ~1008 A      |

### Reference

Riyadh Cables IEC 60287 calculation (duct bank case)

---

## 🧠 Key Notes

* AC resistance is converted from Ω/km → Ω/m before ampacity calculation
* Thermal model follows IEC decomposition (not simplified lumped model)
* Model currently assumes:

  * single circuit
  * flat formation
  * simplified geometry for correction factors

---

## ⚠️ Limitations (Current Version)

* T'''''4 (soil ↔ backfill correction) not yet implemented
* Grouping effects partially simplified
* Some geometric parameters are hardcoded (temporary)
* No GUI / user input interface yet

---

## 🚀 Next Steps

* Implement full T'''''4 correction
* Generalize installation inputs (remove hardcoding)
* Add multiple validation cases
* Refactor architecture (modular separation)

---

## 🏷 Version

v1.0-iec60287-ductbank
Validated against reference calculation (~2% deviation)

---

## 👤 Author

Atiq ur Rahman
