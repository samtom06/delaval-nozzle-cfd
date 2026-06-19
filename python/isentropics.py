def stagnation_temp_ratio(M, gamma):
    ratio = 1 + ((gamma - 1) / 2) * M ** 2
    return ratio

def stagnation_pressure_ratio(M, gamma):
    ratio = (1 + ((gamma - 1) / 2) * M ** 2) ** (gamma / (gamma - 1))
    return ratio

def stagnation_density_ratio(M, gamma):
    ratio = (1 + ((gamma - 1) / 2) * M ** 2) ** (1 / (gamma - 1))
    return ratio

print(f"Stagnation Temp Ratio: {stagnation_temp_ratio(2.0, 1.4):.3f}")
print(f"Stagnation Pressure Ratio: {stagnation_pressure_ratio(2.0, 1.4):.3f}")
print(f"Stagnation Density Ratio: {stagnation_density_ratio(2.0, 1.4):.3f}")

def area_ratio(M, gamma):
    ratio = 1 / M * (2 / (gamma + 1) * (1 + (gamma - 1) / 2 * M ** 2)) ** ((gamma + 1) / (2 * (gamma - 1)))
    return ratio

print(f"Area Ratio: {area_ratio(2, 1.4):.3f}")

def nozzle_section(area_ratio):
    if area_ratio > 1:
        return "Converging or Diverging Area"
    elif area_ratio == 1:
        return "Throat"
    else:
        return "Invalid, the ratio cannot be below the minimum, the throat"

print(f"Area Ratio for Mach 2 & Heat Capacity Ratio 1.4: {nozzle_section(area_ratio(2, 1.4))}")
 