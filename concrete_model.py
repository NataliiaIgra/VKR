from math import sqrt


def calculate_concrete(comp_strength_dash):
    strains = list()
    stresses = list()
    comp_strength_double_dash = 0.9 * comp_strength_dash
    limiting_strain = 0.0038
    concrete_modulus = 57000 * sqrt(comp_strength_dash * 1000) / 1000
    apex_strain = 1.8 * comp_strength_double_dash / concrete_modulus
    parabola_points = 100
    strain_increment = apex_strain / parabola_points
    for i in range(0, parabola_points + 1):
        calculated_strain = i * strain_increment
        strains.append(calculated_strain)
        calculated_stress = comp_strength_double_dash * (
                2 * calculated_strain / apex_strain - (calculated_strain / apex_strain) ** 2)
        stresses.append(calculated_stress)
    strains.append(limiting_strain)
    stresses.append(0.85 * comp_strength_double_dash)
    return strains, stresses
