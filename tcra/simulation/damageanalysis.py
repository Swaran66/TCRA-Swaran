"""
The tsnet.network.geometry read in the geometry defined by EPANet
.inp file, and assign additional parameters needed in transient
simulation later in tsnet.

"""


def generate_fragility_curve(mu, sigma, intensity):
    """Generate the fragility curve using log-normal distribution."""
    return lognorm.cdf(intensity, s=sigma, scale=mu)

def estimate_damage(fragility_curves, building_data):
    """Estimate damage probabilities for all buildings."""
    results = []
    for _, row in building_data.iterrows():
        building_type = row['type']
        intensity = row['mph']
        
        fragility_curves_building = fragility_curves.get(building_type, {})
        building_probabilities = {}
        for damage_state, fragility_params in fragility_curves_building.items():
            fragility_curve = generate_fragility_curve(fragility_params['mu'], fragility_params['sigma'], intensity)
            building_probabilities[damage_state] = fragility_curve
        building_probabilities['id'] = row['id']
        building_probabilities['x'] = row['x']
        building_probabilities['y'] = row['y']
        building_probabilities['mph'] = row['mph']
        building_probabilities['type'] = row['type']
        results.append(building_probabilities)
    return pd.DataFrame(results)

def sample_damage_state(Pr, DStates):
    """Sample the damage state based on probabilities."""
    p = pd.Series(data=np.random.uniform(size=Pr.shape[0]), index=Pr.index)
    damage_state = pd.Series(data=[None] * Pr.shape[0], index=Pr.index)

    for DS_name in DStates:
        damage_state[p < Pr[DS_name]] = DS_name

    return damage_state


# # Assuming fragility_curves is imported or defined
# fragility_curves = {
#     'PW': {
#         'Fail': {'mu': 130.139, 'sigma': 0.1213}
#     },
#     'PS': {
#         'Fail': {'mu': 130.504, 'sigma': 0.1352}
#     }
# }

# building_data = pd.DataFrame({
#     'id': [1, 2],
#     'x': [10, 20],
#     'y': [20, 30],
#     'mph': [120, 125],
#     'type': ['PW', 'PS']
# })

# # Example usage
# estimated_damage = estimate_damage(fragility_curves, building_data)
# print(estimated_damage)

# # Example for sampling damage state
# Pr = pd.DataFrame({
#     'Fail': [0.2, 0.4]
# })

# DStates = ['Fail']

# sampled_damage_state = sample_damage_state(Pr, DStates)
# print(sampled_damage_state)
