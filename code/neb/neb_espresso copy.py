import os
import sys
import numpy as np

from espresso import iEspresso, Espresso
from espresso.nebespresso import NEBEspresso
from ase.optimize.fire import FIRE as QuasiNewton

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

# def printer():
#     global i
#     i += 1
#     print(i)
#     data = str(0)
#     d = data
#     data = Object()
#     data.write = d
#     return data

# class Object():
#     pass

# Import File
file = '/home/camgur/Documents/Coding/Goward/MACE/lattice/LiAlO2_430184.cif'
filename = os.path.basename(file)
base = '/home/camgur/Documents/Coding/Goward/MACE/elastic/LiAlO2/'

# Importing CIF
atoms = read(file)

'''
    command='mpiexec -oversubscribe -n 12 pw.x', 
    pseudo_dir='/home/camgur/Documents/Coding/Goward/ml_nmr/pseudo')
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
'''

# Set Espresso
calculator = iEspresso(
    outdir='/home/camgur/Documents/Coding/Goward/ml_nmr/neb/out/',
    psppath='/home/camgur/Documents/Coding/Goward/ml_nmr/pseudo',
    kpts=(7, 7, 6),
    pw=600,
    verbose='high',
    xc='PBE',
    occupations='smearing',
    smearing='gauss',
    sigma=1.5e-2,
    convergence={'energy': 1e-6, 'mixing': 0.4, 'maxsteps': 100, 'diag': 'david'}
)
atoms.calc = calculator

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



# Setup NEB
images = [initial]
for _ in range(5):
    image = initial.copy()
    image.calc = calculator
    images.append(image)
images.append(final)
neb = NEBEspresso(images, climb=True, allow_shared_calculator=True)
neb.interpolate('idpp')

fig, ax = plt.subplots()
# Set calculators:
for image in images:
    plot_atoms(image, ax, radii=0.2, rotation=('90x,90y,90z'))
    # view(image)
plt.show()

# Optimize:
i = 0
optimizer = QuasiNewton(neb, logfile='./Goward/MACE/elastic/LiAlO2/neb_esp.log', trajectory='./Goward/MACE/elastic/LiAlO2/neb_esp.traj')
# optimizer.attach(printer())
optimizer.run(fmax=0.05)
