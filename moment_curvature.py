from math import sqrt


class Calculation:
    def __init__(self, concrete_model, steel_model, section_model):
        self.concrete_model = concrete_model
        self.steel_model = steel_model
        self.section_model = section_model

    def calculate_moment_curvature(self, section_type):
        if section_type == 'Rectangular':
            depth = self.section_model.depth
            width = self.section_model.width
            cover = self.section_model.cover
            diameter_of_rebar = self.section_model.diameter
            area_of_one_rebar = self.section_model.area
            number_bottom = self.section_model.number_rebars_bottom
            number_top = self.section_model.number_rebars_top

            comp_strength_dash = self.concrete_model.comp_strength_dash

            steel_modulus = self.steel_model.steel_modulus
            yield_strength = self.steel_model.yield_strength

            gross_moment_of_inertia = depth ** 3 * width / 12
            modulus_of_rupture = 7.5 * sqrt(comp_strength_dash * 1000) / 1000
            distance_to_tension_fiber = depth / 2
            cracking_moment = modulus_of_rupture * gross_moment_of_inertia / distance_to_tension_fiber
            concrete_modulus = 57000 * sqrt(comp_strength_dash * 1000) / 1000
            curvature_at_cracking_moment = cracking_moment / (concrete_modulus * gross_moment_of_inertia)

            # Yielding point
            modular_ratio = steel_modulus / concrete_modulus  # TODO
            # singly-reinforced section

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
                                  area_compression_rebars * stress_comp_steel * (
                                              distance_to_As_dash - k * distance_to_As / 3)
                # For ultimate point
                depth_neutral_axis = 0
                depth_neutral_axis_trial = distance_to_As / 4
                tension_steel_force = area_tension_rebars * yield_strength

                while abs(depth_neutral_axis / depth_neutral_axis_trial - 1) > 0.0001:
                    strain_comp_steel = (
                                                    depth_neutral_axis_trial - distance_to_As_dash) / depth_neutral_axis_trial * 0.003
                    stress_comp_steel = steel_modulus * strain_comp_steel
                    comp_steel_force = area_compression_rebars * stress_comp_steel
                    depth_neutral_axis = (tension_steel_force - comp_steel_force) / (
                                0.85 * comp_strength_dash * width * b1)
                    depth_neutral_axis_trial = (depth_neutral_axis_trial + depth_neutral_axis) / 2

                ultimate_moment = 0.85 * comp_strength_dash * b1 * depth_neutral_axis * width * (
                        distance_to_As - b1 * depth_neutral_axis / 2) + area_compression_rebars * stress_comp_steel * (
                                          distance_to_As - distance_to_As_dash)

            curvature_at_yielding_moment = yield_strain / (distance_to_As - k * distance_to_As)
            curvature_at_ultimate_moment = 0.003 / depth_neutral_axis

            curvatures = [0, curvature_at_cracking_moment, curvature_at_yielding_moment, curvature_at_ultimate_moment]
            moments = [0, cracking_moment, yielding_moment, ultimate_moment]

            return curvatures, moments
