from ase.io import read, write
from ase.visualize import view
from ase.io import Trajectory

# From: https://wiki.fysik.dtu.dk/ase/ase/visualize/visualize.html

# Set import and add atoms
file = read('MACE\elastic\LFVO\LFVO_neb.traj@-7:')

view(file)