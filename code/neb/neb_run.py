from mace.calculators import MACECalculator
from ase.optimize import BFGS

from ase import atoms
from ase.atoms import *
from ase.io import *

from ase.mep import NEB

import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms
from ase.visualize import view


atoms = read('MACE/materials/Li3Fe2PO43_98361.cif')
calculator = MACECalculator(model_paths='MACE/2024-01-07-mace-128-L2_epoch-199.model',
                            dispersion=False, device='cuda', default_dtype='float64')
atoms.calc = calculator

# Start NEB method

# Set initial and final states
initial, final = 0, 0

print('\nChoose two atoms for the NEB method\n')
# Interactively ask for user input
while True:
    initial, final = atoms.copy(), atoms.copy()
    initial.edit()
    final.edit()

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
    for q, e in zip(initial, final):
        if (q.position != e.position).any():
            print('Index of Interest: ', q.index)

    # Setup NEB
    images = [initial]
    images += [initial.copy() for i in range(5)]
    images += [final]
    neb = NEB(images, climb=True)
    # Interpolate the potisions linearly
    neb.interpolate()
    
    # Visualise the pathway
    view(images)
    fig, ax = plt.subplots()
    for image in images:
        plot_atoms(image, ax, radii=0.2, rotation=('90x,90y,90z'))
    plt.show()

    # Confirm to continue or decline and choose new atoms
    yesno = input('Continue? y/n\n')
    if yesno == 'y':
        break



# Run optimisation of initial and final
for image in [initial, final]:
    image.calc = calculator
    optimizer = BFGS(image, trajectory=None)
    optimizer.run(fmax=1e-5)



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
# plt.show()

# Optimize:
optimizer = BFGS(neb, trajectory='placeholder')
optimizer.run()

print('Neb Finished!')