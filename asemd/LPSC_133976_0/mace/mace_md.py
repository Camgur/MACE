import sys
import os

from ase import atoms
from ase.io import read
from ase.units import fs
from ase.build import make_supercell

from ase.md.nvtberendsen import NVTBerendsen
from ase.md.bussi import Bussi
from mace.calculators import MACECalculator
import warnings
warnings.filterwarnings("ignore", module="pymatgen")
warnings.filterwarnings("ignore", module="ase")

# Set File
file = sys.argv[1]
filename = os.path.basename(file)
base = '/home/cgurwell/scratch/asemd/' + filename.replace('.cif', '') + '/mace/'

# Importing CIF
atoms = read(file)
atoms = make_supercell(atoms, ((2, 0, 0), (0, 2, 0), (0, 0, 4)), order='atom-major')

# Setting the MACE-MP-0 Calculator
calculator = MACECalculator(model_paths='/home/cgurwell/projects/rrg-ravh011/cgurwell/opt/2024-01-07-mace-128-L2_epoch-199.model',
                            dispersion=False, device='cuda', default_dtype='float64')
atoms.calc = calculator

# Initial relaxation
init = NVTBerendsen(
    atoms=atoms,
    temperature=float(sys.argv[2]),  # in K, set by slurm
    timestep=5*fs,  # in femto-seconds
    taut=100*fs,    # 100 * timestep ideally
    logfile=base + 'md_' + str(sys.argv[2]).replace('.', '_') + '_relaxation_' + filename.replace('.cif', '.log'),
    loginterval=500,
)
init.run(10000)  # 10 ps

# Full run from relaxation
md = Bussi(
    atoms=atoms,
    temperature=float(sys.argv[2]),  # in K, set by slurm
    timestep=2*fs,  # in femto-seconds
    taut=200*fs,    # 100 * timestep ideally
    trajectory=base + 'md_' + str(sys.argv[2]).replace('.', '_') + '_' + filename.replace('.cif', '.traj'),
    logfile=base + 'md_' + str(sys.argv[2]).replace('.', '_') + '_' + filename.replace('.cif', '.log'),
    loginterval=100,
)
md.run(100000)  # run MD simulation