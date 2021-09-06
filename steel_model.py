def calculate_steel(yield_strength, steel_modulus):
    strains = [0, yield_strength / steel_modulus, 0.05]
    stresses = [0, yield_strength, yield_strength]
    return strains, stresses
