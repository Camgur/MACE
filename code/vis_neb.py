from ase.io import read, write
from ase.visualize import view
from ase.io import Trajectory

# From: https://wiki.fysik.dtu.dk/ase/ase/visualize/visualize.html

# Set import and add atoms
file = read('MACE\materials\LAGP_36779.traj@-7:')

view(file)

i = 0
for image in file:
    write('MACE\materials\LAGP_36779' + str(i) + '.cif')
    i += 1