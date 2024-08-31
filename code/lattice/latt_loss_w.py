import os
import numpy as np
import csv

from mace.calculators import MACECalculator
from ase.optimize import BFGS

from ase import atoms
from ase.io import *

from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter
from ase.geometry.cell import *

# https://docs.matlantis.com/atomistic-simulation-tutorial/en/

'''
This code is intended to assess the lattice parameter optiisation
from MACE as a loss function, to return optimal parameters more
similar to the parent atomic system. Materials Project database
should be an optimal source of crystals, as they have been double-
refined, both in cell and atomic parameters.

Setup: Given a cell, optimise the geometry and return new cell
parameters as y_pred. Compare with old cell parameters (y) to
evaluate the loss function.

'''

# Define Simple Loss Function
def loss(atoms):

    return origin - cell_to_cellpar(atoms.cell)


# Define CSV Writer
def writer():
    with open(base + filename.replace('.cif', '.csv'), 'a', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(loss(atoms))
        f.close()
    # Attach write attribute to allow dyn.attach
    # THIS IS REALLY GROSS CODE, HELP
    data = Object()
    data.write = iterable
    return data

# Define a function that does nothing to be iterable above
def iterable():
    pass

# Set to object to allow attaching write in writer func
class Object(object):
    pass


# Import File
file = 'C:\\Users\\camgu\\Goward\\Code\\MACE\\lattice\\LiAlO2_430184.cif'
filename = os.path.basename(file)
base = 'C:\\Users\\camgu\\Goward\\Code\MACE\\lattice\\'
with open(base + filename.replace('.cif', '.csv'), 'w') as f:
    wrt = csv.writer(f, delimiter=',')
    wrt.writerow(['a', 'b', 'c', 'alpha', 'beta', 'gamma'])
    f.close()

# Importing CIF
atoms = read(file)
atoms.calc = MACECalculator(model_paths='C:\\Users\\camgu\\Goward\\Code\\MACE\\2024-01-07-mace-128-L2_epoch-199.model',
                            dispersion=False, device='cuda', default_dtype='float64')
atoms.set_constraint(FixSymmetry(atoms))
origin = cell_to_cellpar(atoms.cell)


# Set Optimise (Atomic and Cell Params)
opt = BFGS(FrechetCellFilter(atoms), trajectory=base + filename.replace('.cif', '.traj'))
opt.attach(writer())


'''
**Requires the object to have .write attribute for dyn.attach**
https://github.com/qsnake/ase/blob/master/ase/optimize/optimize.py

def attach(self, function, interval=1, *args, **kwargs):
    """Attach callback function.

    At every *interval* steps, call *function* with arguments
    *args* and keyword arguments *kwargs*."""

    if not hasattr(function, '__call__'):
        function = function.write
    self.observers.append((function, interval, args, kwargs))
'''


# Run Optimise
opt.run(fmax=1e-4, steps=50)
atoms.write(base + filename.replace('.cif', '_opt.cif'))

print('Finished Opt')

'''
MACE Model Training:

https://mace-docs.readthedocs.io/en/latest/guide/training.html
https://mace-docs.readthedocs.io/en/latest/examples/training_examples.html

'''