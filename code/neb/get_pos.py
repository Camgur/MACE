import matplotlib.pyplot as plt
import numpy as np

from mace.calculators import MACECalculator
from ase.io import read, Trajectory
from ase.mep import NEBTools

# Getting images for proposed NEB
images = read('/home/camgur/Documents/Coding/Goward/MACE/elastic/LiAlO2/neb.traj@-7:')
names = ['FIRST_IMAGE']
names += ['INTERMEDIATE_IMAGE' for i in range(len(images) - 2)]
names += ['LAST_IMAGE']
print('BEGIN_POSITIONS')

for image in images:
    print(names[images.index(image)], '\n')
    print('ATOMIC_POSITIONS angstrom')
    for a, z in zip(image.positions, image.get_chemical_symbols()):
        print(z, '\t', *np.round(a, 6))

print('\nEND_POSITIONS')