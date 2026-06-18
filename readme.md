# Cable Ampacity Model (IEC 60287)

## Overview

This project implements a steady-state cable ampacity calculation workflow based on IEC 60287 methodology.

It models electrical losses and thermal resistances to estimate the allowable current for a power cable under selected installation conditions.

The current validated case is focused on a single-core HV cable installed in a concrete duct bank.

---

## Methodology

The ampacity is calculated using:

```text
I = sqrt(delta_theta / (R_ac * T_total))
```

Where:

```text
delta_theta = conductor temperature - ambient temperature
R_ac        = AC resistance of conductor, ohm/m
T_total     = total thermal resistance, K.m/W
```

The project calculates `R_ac` in `ohm/km`, then converts it to `ohm/m` before evaluating ampacity.

---

## Project Structure

```text
src/models/        Input and output data objects
src/electrical/    IEC 60287 electrical resistance calculations
src/thermal/       IEC 60287 thermal resistance calculations
src/calculations/  High-level ampacity calculation engine
src/standards/     IEC constants and lookup tables
src/gui/           PySide6 desktop GUI
src/utilis/        Terminal result display helpers
```

---

## Model Components

### Electrical Model

The electrical model includes:

```text
DC resistance, temperature corrected
Skin effect factor, ys
Proximity effect factor, yp
AC resistance
```

The AC resistance is calculated as:

```text
R_ac = R_dc * (1 + ys + yp)
```

### Thermal Model

The total thermal resistance is:

```text
T_total = T1 + T2 + T3 + T4
```

Internal thermal resistances:

```text
T1 = conductor to sheath
T2 = sheath to armour
T3 = outer jacket
```

For concrete duct bank installation, external resistance `T4` is decomposed into:

```text
T4_air_gap
T4_duct
T4_external
T4_backfill_concrete_correction
```

---

## GUI Features

The PySide6 GUI currently supports editing:

```text
Cable layer diameter/thickness
Cable spacing
Installation depth
Concrete duct bank number of cables
Concrete duct bank short side
Concrete duct bank long side
Concrete duct bank top cover
Concrete thermal resistivity
Backfill thermal resistivity
```

After each update, the GUI recalculates ampacity through the same calculation engine used by the command-line workflow.

The GUI also displays:

```text
Cable cross-section
Ampacity
AC resistance
T1
T4 total
```

---

## Reference Case

This implementation is validated against a real engineering calculation:

```text
Cable: 1 x 1200 mm2 Cu XLPE, 110 kV
Installation: Concrete duct bank
Formation: Flat
Spacing: 400 mm
Depth: 1450 mm reference case, 1600 mm current default in main.py
Duct: 200 / 225 mm, inner / outer
Soil resistivity: 1.2 K.m/W
Conductor temperature: 90 degC
```

Reference results:

| Parameter | Value |
| --- | --- |
| AC Resistance | 0.01952 ohm/km |
| T1 | 0.378 |
| T3 | 0.051 |
| T4 | approximately 3.10 |
| Ampacity | approximately 1008 A |

Reference source:

```text
Riyadh Cables IEC 60287 calculation, duct bank case
```

---

## Current Limitations

The current version still has some simplified assumptions:

```text
Single circuit
Flat formation
Concrete duct bank installation
Some geometric correction factors are simplified
Some ambient assumptions are still hardcoded
Trefoil formation is not implemented yet
Multiple circuit grouping is not fully implemented yet
```

---

## Next Steps

Planned improvements:

```text
Add trefoil installation support
Add direct buried installation support
Add duct material and duct size GUI inputs
Add temperature and soil resistivity GUI inputs
Add multiple validation cases
Improve input validation and error messages
Generate engineering reports
```

---

## Version

```text
v1.1-iec60287-ductbank-gui
```

---

## Author

Atiq ur Rahman

Powered by AtiqLabs
