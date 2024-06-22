"""
The tsnet.network package contains methods to define
1. a water network geometry,
2. network topology,
3. network control, and
4 .spatial and temporal discretization.

"""
import wntr
import numpy as np
import warnings
from tsnet.utils import calc_parabola_vertex
import folium
import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap
