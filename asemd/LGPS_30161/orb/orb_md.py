import sys
import os

from ase import atoms
from ase.io import read
from ase.units import fs
from ase.build import make_supercell

from ase.md.nvtberendsen import NVTBerendsen
from ase.md.bussi import Bussi
from orb_models.forcefield import pretrained
from orb_models.forcefield.calculator import ORBCalculator
import warnings
warnings.filterwarnings("ignore", module="pymatgen")
warnings.filterwarnings("ignore", module="ase")

# Set File
file = sys.argv[1]
filename = os.path.basename(file)
base = '/home/cgurwell/scratch/asemd/' + filename.replace('.cif', '') + '/orb/'

# Importing CIF
atoms = read(file)
atoms = make_supercell(atoms, ((2, 0, 0), (0, 2, 0), (0, 0, 2)), order='atom-major')

# Setting the Calculator
orbff = pretrained.orb_v2(weights_path='/home/cgurwell/projects/rrg-ravh011/cgurwell/opt/orb-v2-20241011.ckpt', device='cuda') # or choose another model using ORB_PRETRAINED_MODELS[model_name]()
calculator = ORBCalculator(orbff, device='cuda')
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