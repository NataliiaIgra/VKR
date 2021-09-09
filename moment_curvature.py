from math import sqrt

DIAMETERS = [(2, 0.25), (3, 0.375), (4, 0.5), (5, 0.625), (6, 0.75), (7, 0.875), (8, 1), (9, 1.128), (10, 1.27),
             (11, 1.41), (14, 1.693), (18, 2.257)]

AREAS = [(2, 0.05), (3, 0.11), (4, 0.20), (5, 0.31), (6, 0.44), (7, 0.60), (8, 0.79), (9, 1), (10, 1.27),
         (11, 1.56), (14, 2.25), (18, 4.00)]


def calculate_moment_curvature(depth, width, comp_strength_dash, yield_strength, steel_modulus, cover, rebar,
                               number_bottom, number_top):
    # Cracking point
    gross_moment_of_inertia = depth ** 3 * width / 12
    modulus_of_rupture = 7.5 * sqrt(comp_strength_dash * 1000) / 1000
    distance_to_tension_fiber = depth / 2
    cracking_moment = modulus_of_rupture * gross_moment_of_inertia / distance_to_tension_fiber
    concrete_modulus = 57000 * sqrt(comp_strength_dash * 1000) / 1000
    curvature_at_cracking_moment = cracking_moment / (concrete_modulus * gross_moment_of_inertia)

    # Yielding point
    modular_ratio = steel_modulus / concrete_modulus  # TODO
    # singly-reinforced section
    # !!! NOT GOOD PART
    diameter_of_rebar = float()
    area_of_one_rebar = float()
    for i in DIAMETERS:
        if rebar == i[0]:
            diameter_of_rebar = i[1]
            break
    for i in AREAS:
        if rebar == i[0]:
            area_of_one_rebar = i[1]
            break
    distance_to_As = depth - cover - diameter_of_rebar / 2
    distance_to_As_dash = cover + diameter_of_rebar / 2
    area_tension_rebars = area_of_one_rebar * number_bottom
    area_compression_rebars = area_of_one_rebar * number_top
    yield_strain = yield_strength / steel_modulus
    ro = area_tension_rebars / (distance_to_As * width)

    # For ultimate point
    if comp_strength_dash <= 4:
        b1 = 0.85
    elif 4 < comp_strength_dash <= 8:
        b1 = 0.85 - 0.05 * (comp_strength_dash * 1000 - 4000) / 1000
    else:
        b1 = 0.65

    if area_compression_rebars == 0:
        k = sqrt(2 * ro * modular_ratio + (ro * modular_ratio) ** 2) - ro * modular_ratio
        yielding_moment = area_tension_rebars * yield_strength * (distance_to_As - k * distance_to_As / 3)
        # For ultimate point
        depth_neutral_axis = area_tension_rebars * yield_strength / (0.85 * comp_strength_dash * width * b1)
        ultimate_moment = area_tension_rebars * yield_strength * (distance_to_As - b1 * depth_neutral_axis / 2)
    else:
        ro_dash = area_compression_rebars / (distance_to_As * width)
        k = sqrt(2 * (ro + ro_dash * distance_to_As_dash / distance_to_As) * modular_ratio +
                 (ro + ro_dash) ** 2 * modular_ratio ** 2) - (ro + ro_dash) * modular_ratio
        stress_comp_steel = (k * distance_to_As - distance_to_As_dash) / (
                distance_to_As - k * distance_to_As) * yield_strength
        yielding_moment = area_tension_rebars * yield_strength * (distance_to_As - k * distance_to_As / 3) + \
                          area_compression_rebars * stress_comp_steel * (distance_to_As_dash - k * distance_to_As / 3)
        # For ultimate point
        depth_neutral_axis = 0
        depth_neutral_axis_trial = distance_to_As / 4
        tension_steel_force = area_tension_rebars * yield_strength

        while abs(depth_neutral_axis / depth_neutral_axis_trial - 1) > 0.0001:
            strain_comp_steel = (depth_neutral_axis_trial - distance_to_As_dash) / depth_neutral_axis_trial * 0.003
            stress_comp_steel = steel_modulus * strain_comp_steel
            comp_steel_force = area_compression_rebars * stress_comp_steel
            depth_neutral_axis = (tension_steel_force - comp_steel_force) / (0.85 * comp_strength_dash * width * b1)
            depth_neutral_axis_trial = (depth_neutral_axis_trial + depth_neutral_axis) / 2

        ultimate_moment = 0.85 * comp_strength_dash * b1 * depth_neutral_axis * width * (
                    distance_to_As - b1 * depth_neutral_axis / 2) + area_compression_rebars * stress_comp_steel * (
                                      distance_to_As - distance_to_As_dash)

    curvature_at_yielding_moment = yield_strain / (distance_to_As - k * distance_to_As)
    curvature_at_ultimate_moment = 0.003 / depth_neutral_axis

    curvatures = [0, curvature_at_cracking_moment, curvature_at_yielding_moment, curvature_at_ultimate_moment]
    moments = [0, cracking_moment, yielding_moment, ultimate_moment]

    return curvatures, moments

# calculate_moment_curvature(24, 20, 4, 60, 29000, 1.615, 10, 4, 0)
