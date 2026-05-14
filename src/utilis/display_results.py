"""
Displays IEC 60287 ampacity calculation results in a
human-readable terminal format.

This utility function is responsible only for presentation
and debugging output.

The purpose of separating result display from the calculation
engine is to maintain clean software architecture by separating:

    - calculation logic
    - engineering data
    - presentation/output formatting

This allows the same calculation engine to be reused by:
    - command-line studies
    - GUI applications
    - PDF report generation
    - future APIs and automation workflows

Input:
    results : AmpacityResults

        Structured engineering result object returned by
        AmpacityEngine.calculate().
"""

def display_results(results):

    print("DC Resistance (Ω/km):",
          round(results.electrical.dc_resistance, 5))

    print("Skin effect ys:",
          round(results.electrical.skin_effect, 5))

    print("Proximity effect yp:",
          round(results.electrical.proximity_effect, 5))

    print("AC Resistance (Ω/km):",
          round(results.electrical.ac_resistance, 5))

    print("T1 =",
          round(results.thermal.T1, 3))

    print("T2 =",
          round(results.thermal.T2, 3))

    print("T3 =",
          round(results.thermal.T3, 3))

    print("T4 (duct) =",
          round(results.thermal.T4_duct, 3))

    print("T4 total =",
          round(results.thermal.T4_total, 3))

    print("Ampacity (A):",
          round(results.ampacity, 3))