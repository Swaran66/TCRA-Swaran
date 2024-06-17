"""
The tsnet.simulation.main module contains function to perform
the workflow of read, discretize, initial, and transient
simulation for the given .inp file.

"""
def get_fragility_curves(pole_type):

    fragility_curves_epn = {
        'PW': {
            'Fail': {'mu': 130.139, 'sigma': 0.1213}
        },
        'PS': {
            'Fail': {'mu': 130.504, 'sigma': 0.1352}
        }
    }
    return fragility_curves_epn.get(pole_type.upper(), {})

# # Example usage:
# pole_type = 'PW'
# fragility_curve = get_fragility_curves(pole_type)
# if fragility_curve:
#     print(f"Mu for {pole_type}: {fragility_curve['Fail']['mu']}")
#     print(f"Sigma for {pole_type}: {fragility_curve['Fail']['sigma']}")
# else:
#     print(f"No fragility curves found for pole type {pole_type}")


