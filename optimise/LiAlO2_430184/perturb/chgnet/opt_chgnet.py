import sys
import os

from chgnet.model.dynamics import CHGNetCalculator

from ase.optimize import BFGS

from ase import atoms
from ase.io import read

from ase.constraints import FixSymmetry

# Set File
file = sys.argv[1]
filename = os.path.basename(file)
base = '/home/cgurwell/scratch/optimise/' + filename.replace('.cif', '') + '/perturb/chgnet/'

# Importing CIF
atoms = read(file)

# Setting the MACE-MP-0 Calculator
calculator = CHGNetCalculator(use_device='cuda')
atoms.calc = calculator

# Replace Al atom with Ga
atoms[4].symbol = 'Ga'

# Run Optimise (No Cell Opt)
opt = BFGS(atoms, trajectory=base + 'opt_' + filename.replace('.cif', '.traj'))
opt.run(fmax=1e-5, steps=400)

atoms.write(base + 'opt_' + filename)