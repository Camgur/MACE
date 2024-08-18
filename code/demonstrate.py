import torch
import numpy as np
import mace

import matplotlib as mpl
import matplotlib.pyplot as plt

from mace.calculators import mace_mp, MACECalculator
from ase.calculators.loggingcalc import LoggingCalculator
from ase.optimize import BFGS

from ase.visualize import view
from ase.visualize.plot import plot_atoms
from ase import build, units, atoms
from ase.io import read, write, Trajectory
from ase.io.animation import write_gif

from ase.constraints import ExpCellFilter, StrainFilter, UnitCellFilter
from ase.spacegroup.symmetrize import FixSymmetry, check_symmetry
from spglib import get_spacegroup

from bvlain import Lain

# Ask for file location
file = str(input('File Location:\n'))

# Importing CIF
atoms = read(file)

# Rename File
file_name = str(file).rsplit('/', 1)[1].replace('.cif', '_opt.cif')

# Setting the MACE-MP-0 Calculator
calculator = MACECalculator(model_paths='/home/camgur/Documents/Coding/Goward/MACEMP0/Resources/2024-01-07-mace-128-L2_epoch-199.model',
                            dispersion=False, device='cuda', default_dtype='float64')
atoms.calc = calculator

# Track Data
nsteps = []
energies = []
log_calc = LoggingCalculator(calculator)

# Set Log
atoms.calc = log_calc

# Set Cell Filter (preserve unit cell symmetry)
atoms.set_constraint(FixSymmetry(atoms))

print("Cell size before: ", atoms.cell)

# Run Optimise
opt = BFGS(UnitCellFilter(atoms), trajectory=file_name.replace('.cif', '.traj'))
opt.run(fmax=1e-4)

print("Cell size after : ", atoms.cell)
atoms.write(file_name)

# Plot Out
plt.figure(figsize=(10,10))
log_calc.plot(markers=['r-', 'b-'], energy=True, lw=2)
plt.show()

# Set BV Calculator
calc = Lain(verbose=True)

# Set State
st = calc.read_file(file)

params = {'mobile_ion': str(input('What is the mobile ion? (Include Charge, e.g. Li1+\n')),    # mobile specie
		  'r_cut': 6.0,           # cutoff for interaction between the mobile species and framework
		  'resolution': 0.1,	   # distance between the grid points
		  'k': 100                 # maximum number of neighbors to be collected for each point
}

# Run Distributions
_ = calc.bvse_distribution(**params)
# _ = calc.void_distribution(**params)

# Perform Percolation Analysis
print(calc.percolation_barriers(encut = 5.0))

# Create Savestate
savestate = file_name.replace('.cif', '_bvel')

# Write Grid File
calc.write_grd(filename = savestate, task = 'bvse')  # saves .grd file

# Check for Mismatches
table = calc.mismatch(r_cut = 4.0)

# MAKE SURE TO SET ISOSURFACE TO 0.4
# MUST SET THE ISOSURFACE TO NEGATIVE

print('Finished!!!')