import warnings
warnings.simplefilter(action='ignore')

import sys
import os

from chgnet.model.dynamics import CHGNetCalculator
from ase.optimize import BFGS

from ase import atoms
from ase.atoms import *
from ase.io import *

from ase.mep import NEB
from ase.optimize import BFGS
from ase.constraints import FixSymmetry

import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms

# Read atoms from CIF passed in arg1
atoms = read(str(sys.argv[1]))
filename = os.path.splitext(os.path.basename(str(sys.argv[1])))[0]
calculator = CHGNetCalculator(model=None, use_device='cuda')
atoms.calc = calculator

atoms.set_constraint(FixSymmetry(atoms))
opt = BFGS(atoms, trajectory=None)
opt.run(fmax=1e-2, steps=100)

# Start NEB method

# Set initial and final states (using arg2, arg3 as atom indices starting from index 0)
atoms.set_constraint()
initial, final = atoms.copy(), atoms.copy()
# init, finl = final[int(sys.argv[3])], initial[int(sys.argv[2])]
del initial[int(sys.argv[3])]
del final[int(sys.argv[2])]

ind = []

# Find unmatched indicies and list
for q, e in zip(initial, final):
    if (q.position != e.position).any():
        ind.append(q.index)

# Save the beginning and ending indices that don't match
ind1 = ind[0]
ind2 = ind[-1]

# Set up indicies correctly
if (initial[ind1].position != atoms[ind1].position).any():
    atm = initial[ind2]
    for i in range(ind1, ind2):
        initial[i].position = final[i].position
    initial[ind1].position = atm.position
    initial[ind2].position = final[ind2].position
else:
    atm = final[ind2]
    for i in range(ind1, ind2):
        final[i].position = initial[i].position
    final[ind1].position = atm.position
    final[ind2].position = initial[ind2].position

# Print Mismatch (there should be only one, ideally)
print('Printing Mismatched Indices (there should be only one):')
for q, e in zip(initial, final):
    if (q.position != e.position).any():
        print('Index: ', q.index)

# Run optimisation of initial and final
for image in [initial, final]:
    image.calc = calculator
    optimizer = BFGS(image, trajectory=None)
    optimizer.run(fmax=1e-3, steps=100)

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
optimizer = BFGS(neb, trajectory=filename + '_chgnet_' + str(sys.argv[2]) + 'to' + str(sys.argv[3]) + '.traj')
optimizer.run(fmax=0.01, steps=200)

print('Neb Finished!')
