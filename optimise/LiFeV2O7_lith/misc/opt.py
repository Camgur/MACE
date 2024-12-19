import sys
import os

from chgnet.model.dynamics import CHGNetCalculator

from ase.optimize import BFGS

from ase import atoms
from ase.io import read

from ase.constraints import FixSymmetry
from ase.spacegroup import get_spacegroup, symmetrize

# Set File
file = 'MACE\optimise\Li3Fe2PO43_98361\LFVO_opt.cif'
filename = os.path.basename(file)
base = 'MACE/optimise/Li3Fe2PO43_98361/'

# Importing CIF
atoms = read(file)

# Setting the Calculator
calculator = CHGNetCalculator(use_device='cuda')
atoms.calc = calculator

# Preserve Unit Cell Symmetry
atoms.set_constraint(FixSymmetry(atoms))

# Run Optimise (No Cell Opt)
opt = BFGS(atoms, trajectory=base + 'opt_' + filename.replace('.cif', '.traj'))
opt.run(fmax=1e-5, steps=400)

atoms.write(base + 'opt_chgnet_' + filename)