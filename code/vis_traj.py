from ase.io import read, write
from ase.visualize import view
from ase.io import Trajectory

# From: https://wiki.fysik.dtu.dk/ase/ase/visualize/visualize.html

# Set import and add atoms
file = Trajectory(str(input('Trajectory Location:\n')))

view(file)