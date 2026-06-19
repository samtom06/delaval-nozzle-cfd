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
    
def run_case (AR, gamma, P_o, T_o, P_ambient, label = None):
    M_exit = solve_mach_from_area (AR, gamma)
    temp_ratio = stagnation_temp_ratio(M_exit, gamma)
    pressure_ratio = stagnation_pressure_ratio (M_exit, gamma)
    exit_temp = T_o / temp_ratio
    R = 287
    exit_velocity = M_exit * np.sqrt(gamma * R * exit_temp)
    g_o = 9.81
    Isp = exit_velocity / g_o
    T_throat = T_o * (2 / (gamma + 1))
    P_throat = P_o * (2 / (gamma + 1)) ** (gamma / (gamma - 1))
    exit_pressure = P_o / pressure_ratio

    if abs(exit_pressure - P_ambient) < 0.01 * exit_pressure:
        regime = "Ideally Expanded."
    elif exit_pressure > P_ambient:
        regime = "Under-expanded."
    else:
        regime = "Over-expanded."

    return{

        "label": label, 
        "area_ratio": AR, 
        "gamma": gamma,
        "P_o": P_o, 
        "T_o": T_o, 
        "P_ambient": P_ambient,
        "M_exit": M_exit, 
        "exit_temp": exit_temp, 
        "exit_pressure": exit_pressure,
        "exit_velocity": exit_velocity, 
        "T_throat": T_throat, 
        "P_throat": P_throat,
        "Isp": Isp, 
        "regime": regime
    }

def print_case(r):
    if r["label"]:
        print(f"~~~ {r['label']} ~~~")
    print(f"Exit Mach: {r['M_exit']:.3f}")
    print(f"Exit Temp: {r['exit_temp']:.1f} K")
    print(f"Exit Pressure: {r['exit_pressure']:.0f} Pa")
    print(f"Exit Velocity: {r['exit_velocity']:.1f} m/s")
    print(f"Throat Temp: {r['T_throat']:.1f} K")
    print(f"Throat Pressure: {r['P_throat']:.0f} Pa")
    print(f"Specific Impulse: {r['Isp']:.1f} s")
    print(f"Regime: {r['regime']}")

cases = [
    run_case(1.6875, 1.4, 500000, 3000, 101325, "Sea Level (101,325 Pa)"),
    run_case(1.6875, 1.4, 500000, 3000, 63902, "Design Altitude (63,902 Pa)"),
    run_case(1.6875, 1.4, 500000, 3000, 20000, "High Altitude (20,000 Pa)")

]

for c in cases:
    print_case(c)

print("~~~ Validation Checks ~~~")
print(f"Area Ratio at M=2: {area_ratio(2, 1.4):.4f}")
print(f"Mach from area ratio 1.6875: {solve_mach_from_area(1.6875, 1.4):.3f}")
print(f"Stagnation Temp Ratio: {stagnation_temp_ratio(2.0, 1.4):.3f}")
print(f"Stagnation Pressure Ratio: {stagnation_pressure_ratio(2.0, 1.4):.3f}")
print(f"Stagnation Density Ratio: {stagnation_density_ratio(2.0, 1.4):.3f}")
print(f"Section at M=2: {nozzle_section(area_ratio(2, 1.4))}")

mach_values = np.linspace (1.05, 5, 200)
area_values = [area_ratio(M, 1.4) for M in mach_values]

mach_sub = np.linspace(0.05, 0.999, 200)
area_sub = [area_ratio(M, 1.4) for M in mach_sub]

plt.plot(mach_sub, area_sub, 'b-')
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



