import sys
import os

from chgnet.model.dynamics import CHGNetCalculator

from ase.optimize import BFGS

from ase import atoms
from ase.io import read

from ase.constraints import FixSymmetry
from ase.filters import ExpCellFilter

# Set File
file = sys.argv[1]
filename = os.path.basename(file)
base = '/home/cgurwell/scratch/optimise/' + filename.replace('.cif', '') + '/chgnet/'

# Importing CIF
atoms = read(file)

# Setting the MACE-MP-0 Calculator
calculator = CHGNetCalculator(use_device='cuda')
atoms.calc = calculator

# Preserve Unit Cell Symmetry
atoms.set_constraint(FixSymmetry(atoms))

# Run Optimise (Cell Opt) allow relaxation of unit cell
opt = BFGS(ExpCellFilter(atoms), trajectory=base + 'opt_' + filename.replace('.cif', '.traj'))
opt.run(fmax=1e-5, steps=400)

atoms.write(base + 'opt_' + filename)