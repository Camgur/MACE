import sys
import os

from mace.calculators import MACECalculator

from ase.optimize import BFGS

from ase import atoms
from ase.io import read

from ase.constraints import FixSymmetry

# Set File
file = sys.argv[1]
filename = os.path.basename(file)
base = '/home/cgurwell/scratch/optimise/' + filename.replace('.cif', '') + '/mace/'

# Importing CIF
atoms = read(file)

# Setting the MACE-MP-0 Calculator
calculator = MACECalculator(model_paths='/home/cgurwell/projects/rrg-ravh011/cgurwell/opt/2024-01-07-mace-128-L2_epoch-199.model',
                            dispersion=False, device='cuda', default_dtype='float64')
atoms.calc = calculator

# Preserve Unit Cell Symmetry
atoms.set_constraint(FixSymmetry(atoms))

# Run Optimise (No Cell Opt)
opt = BFGS(atoms, trajectory=base + 'opt_' + filename.replace('.cif', '.traj'))
opt.run(fmax=1e-5, steps=400)

atoms.write(base + filename)
