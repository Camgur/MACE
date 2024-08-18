import sys, os
import numpy as np
import pandas as pd

from ase.io import read
from ase import atoms
from ase import units

from mace.calculators import MACECalculator

from ase.md.velocitydistribution import MaxwellBoltzmannDistribution
from ase.md import MDLogger
from ase.md import Langevin

# Set file input
file = sys.argv[1]
filename = os.path.basename(file).replace('.cif', '')
base = '/home/cgurwell/scratch/aseMD/'
logfile = base + filename + '_md' + '.log'

# Read atoms object
atoms = read(file)

# Erase previous file contents
try:
    open(logfile, 'w').close()
finally:
    pass

# Set calculator
calculator = MACECalculator(model_paths='/home/cgurwell/projects/rrg-ravh011/cgurwell/Ion_Channels/2024-01-07-mace-128-L2_epoch-199.model',
                            dispersion=True, device='cuda', default_dtype='float64')
atoms.calc = calculator

# Set Maxwell-Boltzmann dist
MaxwellBoltzmannDistribution(atoms, temperature_K=298.)

# Set Langevin dynamics simulation
dyn = Langevin(atoms, timestep=0.5*units.fs, temperature_K=298., 
               friction=1e-4, trajectory=logfile.replace('.log', '.traj'))
dyn.attach(MDLogger(dyn=dyn, atoms=atoms, logfile=logfile, 
                    header=True, stress=True, peratom=True, mode="a"), interval=100)

# Run dynamics sim
dyn.run(10000)