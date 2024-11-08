import sys
import os

from mace.calculators import MACECalculator
from ase.optimize import BFGS

from ase import atoms
from ase.atoms import *
from ase.io import *

from ase.mep import NEB
from ase.optimize import BFGS

import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms

# Save lithiated CIF
lithiated = read(str(sys.argv[4]))

# Read atoms from CIF passed in arg1
atoms = read(str(sys.argv[1]))
filename = os.path.splitext(os.path.basename(str(sys.argv[1])))[0]
calculator = MACECalculator(model_paths='/home/cgurwell/projects/rrg-ravh011/cgurwell/Ion_Channels/2024-01-07-mace-128-L2_epoch-199.model',
                            dispersion=False, device='cuda', default_dtype='float64')
atoms.calc = calculator

# Start NEB method

# Set initial and final states (using arg2, arg3 as atom indices starting from index 0)
initial, final = atoms.copy(), atoms.copy()
initial.append(lithiated[int(sys.argv[2])].symbol)
initial[-1].position = lithiated[int(sys.argv[2])].position
final.append(lithiated[int(sys.argv[3])].symbol)
final[-1].position = lithiated[int(sys.argv[3])].position

# Run optimisation of initial and final
for image in [initial, final]:
    image.calc = calculator
    optimizer = BFGS(image, trajectory=None)
    optimizer.run(fmax=1e-5)

# Setup NEB
images = [initial]
images += [initial.copy() for i in range(10)]
images += [final]
neb = NEB(images, climb=True, allow_shared_calculator=True)
# Interpolate the potisions linearly
neb.interpolate()

fig, ax = plt.subplots()
# Set calculators:
for image in images:
    image.calc = calculator
    plot_atoms(image, ax, radii=0.2, rotation=('35x,35y,0z'))
plt.savefig(filename + '_' + str(sys.argv[2]) + 'to' + str(sys.argv[3]) + '.png')

# Optimize:
optimizer = BFGS(neb, trajectory=filename + '_' + str(sys.argv[2]) + 'to' + str(sys.argv[3]) + '.traj')
optimizer.run()

print('Neb Finished!')