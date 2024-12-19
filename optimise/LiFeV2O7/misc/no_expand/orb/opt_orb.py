import sys
import os

from orb_models.forcefield import pretrained
from orb_models.forcefield.calculator import ORBCalculator

from ase.optimize import BFGS

from ase import atoms
from ase.io import read

from ase.constraints import FixSymmetry

# Set File
file = sys.argv[1]
filename = os.path.basename(file)
base = '/home/cgurwell/scratch/optimise/' + filename.replace('.cif', '') + '/orb/'

# Importing CIF
atoms = read(file)

# Setting the MACE-MP-0 Calculator
orbff = pretrained.orb_v2(weights_path='/home/cgurwell/projects/rrg-ravh011/cgurwell/opt/orb-v2-20241011.ckpt', device='cuda') # or choose another model using ORB_PRETRAINED_MODELS[model_name]()
calculator = ORBCalculator(orbff, device='cuda')
atoms.calc = calculator

# Preserve Unit Cell Symmetry
atoms.set_constraint(FixSymmetry(atoms))

# Run Optimise (Cell Opt) allow relaxation of unit cell
opt = BFGS(ExpCellFilter(atoms), trajectory=base + 'opt_' + filename.replace('.cif', '.traj'))
opt.run(fmax=1e-5, steps=400)

atoms.write(base + 'opt_' + filename)
