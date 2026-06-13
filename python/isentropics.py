import numpy as np
import matplotlib.pyplot as plt

from scipy.optimize import brentq   # type: ignore

def solve_mach_from_area (target_area_ratio, gamma):
    M_solution = brentq(lambda M: area_ratio(M, gamma) - target_area_ratio, 1.05, 50)
    return M_solution

def stagnation_temp_ratio(M, gamma):
    ratio = 1 + ((gamma - 1) / 2) * M ** 2
    return ratio

def stagnation_pressure_ratio(M, gamma):
    ratio = (1 + ((gamma - 1) / 2) * M ** 2) ** (gamma / (gamma - 1))
    return ratio

def stagnation_density_ratio(M, gamma):
    ratio = (1 + ((gamma - 1) / 2) * M ** 2) ** (1 / (gamma - 1))
    return ratio

def area_ratio (M, gamma):
    ratio = 1 / M * (2 / (gamma + 1) * (1 + (gamma - 1) / 2 * M ** 2)) ** ((gamma + 1) / (2 * (gamma - 1)))
    return ratio

def nozzle_section(area_ratio):
    if area_ratio > 1:
        return "Converging or Diverging Area"
    elif area_ratio == 1:
        return "Throat"
    else:
        return "Invalid, the ratio cannot be below the minimum, the throat"
    
def run_case (area_ratio, gamma, P_o, T_o, P_ambient):
    M_exit = solve_mach_from_area (area_ratio, gamma)
    temp_ratio = stagnation_temp_ratio(M_exit, gamma)
    pressure_ratio = stagnation_pressure_ratio (M_exit, gamma)
    exit_temp = T_o / temp_ratio
    exit_pressure = P_o / pressure_ratio
    if abs(exit_pressure - P_ambient) < 1:
        regime = "Ideally Expanded."
    elif exit_pressure > P_ambient:
        regime = "Under-expanded."
    else:
        regime = "Over-expanded."
    print(f"Exit Mach: {M_exit:.3f}")
    print(f"Exit Temp: {exit_temp:.1f} K")
    print(f"Exit Pressure: {exit_pressure:.0f} Pa")
    print(f"Regime: {regime}")

print("~~~ Sea Level (101,325 Pa) ~~~")
run_case(1.6875, 1.4, 500000, 3000, 101325) 
print("~~~ Design Altitude (63,902 Pa) ~~~")
run_case(1.6875, 1.4, 500000, 3000, 63902)
print("~~~ High Altitude (20,000 Pa) ~~~")
run_case(1.6875, 1.4, 500000, 3000, 20000)

print("~~~ Validation Checks ~~~")

print(f"Area Ratio: {area_ratio(2, 1.4):.4f}")

print(f"Mach from area ratio 1.6875: {solve_mach_from_area(1.6875, 1.4):.3f}")

print(f"Stagnation Temp Ratio: {stagnation_temp_ratio(2.0, 1.4):.3f}")
print(f"Stagnation Pressure Ratio: {stagnation_pressure_ratio(2.0, 1.4):.3f}")
print(f"Stagnation Density Ratio: {stagnation_density_ratio(2.0, 1.4):.3f}")

print(f"Area Ratio for Mach 2 & Heat Capacity Ratio 1.4: {nozzle_section(area_ratio(2, 1.4))}")

mach_values = np.linspace (1.05, 5, 200)
area_values = [area_ratio(M, 1.4) for M in mach_values]

plt.plot(mach_values, area_values)
plt.xlabel("Mach"), plt.ylabel("A/A*"), plt.title("Area vs. Mach Curve")
plt.grid(True)
plt.plot(2.0, 1.6875, 'ro')
plt.show()

"""

This was SO. MUCH. FUN. First time really seeing how well Python integrates
into my structure, and fully understanding how these tools aid us
as engineers. Validating it against theory and seeing it be correct 
(after much trial and error) was extremely gratifying haha.

"""



