import numpy as np
from ase.io import read, write
from ase.visualize import view
from ase.io import Trajectory

from ase.md.analysis import DiffusionCoefficient

# From: https://wiki.fysik.dtu.dk/ase/ase/visualize/visualize.html

# Set import and add atoms
file = Trajectory(str(input('Trajectory Location:\n')))

# Uses Einstein's method, probably not so great
D = DiffusionCoefficient(file, timestep=100, atom_indices=[120, 121, 122, 123], molecule=False)
D.plot(show=True)

view(file)