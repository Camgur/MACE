import os
import sys
import numpy as np

from ase.calculators.espresso import Espresso, EspressoProfile
from ase.optimize import BFGS

from ase import atoms
from ase.atoms import *
from ase.io import *

from ase.neb import NEB
# from ase.spacegroup.symmetrize import FixSymmetry

import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms

'''
Setup the initial conditions of the NEB method
(i.e., choose which atom to remove for end and
beginning of the NEB method).

Goals: User gets to choose directly which atom
is removed. NEB should do everything from there.

https://github.com/lmmentel/ase-espresso

'''
np.set_printoptions(threshold=sys.maxsize, edgeitems=100000)

def printer():
    global i
    i += 1
    print(i)
    data = str(0)
    d = data
    data = Object()
    data.write = d
    return data

class Object():
    pass

# Import File
file = '/home/camgur/Documents/Coding/Goward/MACE/lattice/LiAlO2_430184.cif'
filename = os.path.basename(file)
base = '/home/camgur/Documents/Coding/Goward/MACE/elastic/LiAlO2/'

# Importing CIF
atoms = read(file)

# Set Espresso
pseudo = {
    'Al': 'Al.pbe-tm-gipaw-dc.UPF', 
    'Li': 'Li.pbe-tm-gipaw-dc.UPF', 
    'O': 'O.pbe-tm-new-gipaw-dc.UPF'}
profile = EspressoProfile(
    command='mpiexec -oversubscribe -n 12 pw.x', 
    pseudo_dir='/home/camgur/Documents/Coding/Goward/espresso/pseudo')
data = {
    'control': {'tstress': True, 'tprnfor': True, 
                'verbosity': 'high', 
                'outdir': '/home/camgur/Documents/Coding/Goward/ml_nmr/neb/out',
                'prefix': 'LiAlO2_e'},
    'system': {'ecutwfc': 80, 'ecutrho': 600,
               'occupations': 'smearing', 
               'degauss': 0.015,
               'smearing': 'cold'},
    'electrons': {'mixing_beta': 0.4}
    }

calculator = Espresso(
    profile=profile,
    pseudopotentials=pseudo,
    kpts=(7, 7, 6),
    input_data=data

)
atoms.calc = calculator

# Set initial and final states
initial, final = 0, 0

print('\nDelete two atoms for the NEB method\n')
# Interactively ask for user input
while True:
    initial, final = atoms.copy(), atoms.copy()
    initial.edit()
    final.edit()
    yesno = input('Continue? y/n\n')
    if yesno == 'y':
        break

# Run optimisation of initial and final
for image in [initial, final]:
    image.calc = calculator
    optimizer = BFGS(image, trajectory=None)
    print('Running opt #', [initial, final].index(image) + 1)
    optimizer.run(fmax=5e-3)
print('Finished opt')

# Setup NEB
images = [initial]
images += [initial.copy() for i in range(5)]
images += [final]
neb = NEB(images, climb=True, allow_shared_calculator=True)
# Interpolate the potisions linearly
neb.interpolate()

# Print the intermediate images for Quantum Espresso (angstroms)
for image in images:
    print('\nImage: ', images.index(image) + 1)
    for a in image.positions:
        print(*np.round(a, 6))