"""
The tsnet.simulation.main module contains function to perform
the workflow of read, discretize, initial, and transient
simulation for the given .inp file.

"""


import numpy as np
import pandas as pd

def calculate_parameters(data):
    Lat = []          # Latitude
    Long = []         # Longitude
    CP = []           # Central Pressure (millibar)
    Δp = []           # Central Pressure Difference (millibar)
    Rmax = []         # Radius to max wind speed (km)
    B = []            # Holland Parameter
    ρ = []            # Air density
    Ω = []            # Earth's angular velocity (rad/s)

    for _, row in data.iterrows():
        Lat_val = row['Lat']
        Long_val = row['Long']
        CP_val = row['CP']
        Δp_val = 1013 - CP_val
        Rmax_val = np.exp(2.556 - 0.000050255 * (Δp_val ** 2) + 0.042243032 * Lat_val)
        B_val = 1.881 - 0.00557 * Rmax_val - 0.01097 * Lat_val

        Lat.append(Lat_val)
        Long.append(Long_val)
        CP.append(CP_val)
        Δp.append(Δp_val)
        Rmax.append(Rmax_val)
        B.append(B_val)
        ρ.append(1.15)
        Ω.append(0.00007292)

    track = {
        'Lat': Lat,
        'Long': Long,
        'CP': CP,
        'Δp': Δp,
        'Rmax': Rmax,
        'B': B,
        'ρ': ρ,
        'Ω': Ω
    }

    df_track = pd.DataFrame(track)
    return df_track

def calculate_wind_speeds(df_track, blg):
    Vmph = []

    for _, hurricane_row in df_track.iterrows():
        Lat_HE = np.radians(hurricane_row['Lat'])
        Long_HE = np.radians(hurricane_row['Long'])
        ρ = hurricane_row['ρ']
        B = hurricane_row['B']
        Rmax = hurricane_row['Rmax'] * 1000
        CP = hurricane_row['CP']
        Δp = hurricane_row['Δp'] * 100

        Vmph1 = []
        Vmph.append(Vmph1)

        for _, building_row in blg.iterrows():
            Lat = building_row['y']
            Long = building_row['x']
            Lat_rad = np.radians(Lat)
            Long_rad = np.radians(Long)
            delLat = Lat_HE - Lat_rad
            delLong = Long_HE - Long_rad

            a = np.sin(delLat / 2)**2 + np.cos(Lat_HE) * np.cos(Lat_rad) * np.sin(delLong / 2)**2
            rr = 2 * 6373 * np.arcsin(np.sqrt(a))
            r = rr * 1000  # Distance from hurricane eye to building

            f = 2 * 0.000073 * np.sin(Lat_rad)  # Coriolis parameter
            Vg = np.sqrt((((Rmax / r)**B) * ((B * Δp * np.exp(-(Rmax / r)**B)) / ρ)) + ((r**2) * (f**2) * 0.25)) - (r * f / 2)
            V = Vg * 2.2369362920544  # m/s to mph

            Vmph1.append(V)

    VG1 = pd.DataFrame(Vmph)
    VG = VG1 * 1.287 * 1.61  # Convert gradient wind speed to gust wind speed
    Vg = VG1.T

    V3s = Vg.max(axis=1) * 0.86 * 1.287  # Use coefficient 0.8-0.86 depending on hurricane intensity
    V3 = list(blg.id)
    vv = list(V3s.values)
    pf = {'ind': V3, 'mph': vv}
    nn = pd.DataFrame(pf)

    bldg_wind = blg.merge(nn, left_on='id', right_on='ind')
    return bldg_wind, VG

