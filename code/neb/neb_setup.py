import os
import sys
import numpy as np

from mace.calculators import MACECalculator
from ase.optimize import BFGS

from ase import atoms
from ase.atoms import *
from ase.io import *

from ase.neb import NEB, DyNEB
from ase.spacegroup.symmetrize import FixSymmetry
from ase.visualize import view

import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms

'''
Setup the initial conditions of the NEB method
(i.e., choose which atom to remove for end and
beginning of the NEB method).

Goals: User gets to choose directly which atom
is removed. NEB should do everything from there.

'''
np.set_printoptions(threshold=sys.maxsize, edgeitems=100000)


# Import File
file = 'C:\\Users\\camgu\\Goward\\Code\\MACE\\lattice\\LiAlO2_430184.cif'
filename = os.path.basename(file)
base = 'C:\\Users\\camgu\\Goward\\Code\\MACE\\elastic\\LiAlO2\\'

# Importing CIF
atoms = read(file)
calculator = MACECalculator(model_paths='C:\\Users\\camgu\\Goward\\Code\\MACE\\2024-01-07-mace-128-L2_epoch-199.model',
                            dispersion=False, device='cpu', default_dtype='float32')
atoms.calc = calculator
atoms.set_constraint(FixSymmetry(atoms))


# Set Optimise (Atomic Params Only)
opt = BFGS(atoms, trajectory=None)

# Run Optimise
opt.run(fmax=1e-2)

print('Finished Opt')



# Start NEB method

# Set ion
ion = 'Li'

# Set lists
symbols = []
positions = []

# Append target ions
for i, n in zip(atoms.symbols, atoms.positions):
    if i == ion:
        symbols.append(i + str(i.index in atoms))
        positions.append(n)

symbols, positions = np.array(symbols), np.array(positions)

# Set initial and final states
atoms.set_constraint()
initial, final = 0, 0

print('\nChoose two atoms for the NEB method\n')
# Interactively ask for user input
while True:
    initial, final = atoms.copy(), atoms.copy()
    initial.edit()
    final.edit()
    yesno = input('Continue? y/n\n')
    print(initial)
    if yesno == 'y':
        break

# Run optimisation of initial and final
for image in [initial, final]:
    image.calc = calculator
    optimizer = BFGS(image, trajectory=None)
    optimizer.run(fmax=1e-4)



# Setup NEB
images = [initial]
images += [initial.copy() for i in range(5)]
images += [final]
neb = NEB(images, climb=True, allow_shared_calculator=True)
# Interpolate the potisions linearly
neb.interpolate()

fig, ax = plt.subplots()
# Set calculators:
for image in images:
    image.calc = calculator
    plot_atoms(image, ax, radii=0.2, rotation=('90x,90y,90z'))
    # view(image)
plt.show()

# Optimize:
optimizer = BFGS(neb, trajectory='MACE\\elastic\\LiAlO2\\neb.traj')
optimizer.run()