import sys
import os

from ase import atoms
from ase.io import read
from ase.units import fs
from ase.build import make_supercell

from ase.md.nvtberendsen import NVTBerendsen
from ase.md.bussi import Bussi
from chgnet.model.dynamics import CHGNetCalculator
import warnings
warnings.filterwarnings("ignore", module="pymatgen")
warnings.filterwarnings("ignore", module="ase")

# Set File
file = r'MACE\asemd\LAGP\chgnet\opt_LAGP.cif'
filename = os.path.basename(file)
base = r'MACE\code\md\test'

# Importing CIF
atoms = read(file)
atoms = make_supercell(atoms, ((2, 0, 0), (0, 2, 0), (0, 0, 2)), order='atom-major')

# Setting the Calculator
calculator = CHGNetCalculator(use_device='cuda')
atoms.calc = calculator


# Initial relaxation
init = NVTBerendsen(
    atoms=atoms,
    temperature=float(300),  # in K, set by slurm
    timestep=5*fs,  # in femto-seconds
    taut=100*fs,    # 100 * timestep ideally
    logfile=base + 'md_' + str(300).replace('.', '_') + '_relaxation_' + filename.replace('.cif', '.log'),
    loginterval=500,
)
init.run(1000)  # 1 ps

# Add printer to signal iteration
i = 0
def printer():
    global i
    i+=1
    print(i)

# Full run from relaxation
md = Bussi(
    atoms=atoms,
    temperature_K=float(300),  # in K, set by slurm
    timestep=2*fs,  # in femto-seconds
    taut=200*fs,    # 100 * timestep ideally
    trajectory=base + 'md_' + str(300).replace('.', '_') + '_' + filename.replace('.cif', '.traj'),
    logfile=base + 'md_' + str(300).replace('.', '_') + '_' + filename.replace('.cif', '.log'),
    loginterval=100,
)

md.attach(printer())
md.run(100000)  # run MD simulation