import os

from orb_models.forcefield import pretrained
from orb_models.forcefield.calculator import ORBCalculator

from ase.optimize import BFGS

from ase import atoms
from ase.io import read

from ase.constraints import FixSymmetry

# Set File
file = 'MACE/materials/LiAlO2_430184.cif'
filename = os.path.basename(file)
base = 'MACE/tests/'

# Importing CIF
atoms = read(file)

# Setting the MACE-MP-0 Calculator
orbff = pretrained.orb_v2(device='cpu') # or choose another model using ORB_PRETRAINED_MODELS[model_name]()
calculator = ORBCalculator(orbff, device='cpu')
atoms.calc = calculator

# Preserve Unit Cell Symmetry
atoms.set_constraint(FixSymmetry(atoms))

# Run Optimise (No Cell Opt)
opt = BFGS(atoms, trajectory=base + 'opt_' + filename.replace('.cif', '.traj'))
opt.run(fmax=1e-5, steps=400)

atoms.write(base + 'opt_' + filename)
