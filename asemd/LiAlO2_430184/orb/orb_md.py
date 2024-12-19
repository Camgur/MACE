import sys
import os

from ase import atoms
from ase.io import read
from ase.units import fs
from ase.build import make_supercell

from ase.md.nvtberendsen import NVTBerendsen
from orb_models.forcefield import pretrained
from orb_models.forcefield.calculator import ORBCalculator
import warnings
warnings.filterwarnings("ignore", module="pymatgen")
warnings.filterwarnings("ignore", module="ase")

# Set File
file = sys.argv[1]
filename = os.path.basename(file)
base = '/home/cgurwell/scratch/asemd/' + filename.replace('.cif', '') + '/chgnet/'

# Importing CIF
atoms = read(file)
atoms = make_supercell(atoms, ((4, 0, 0), (0, 4, 0), (0, 0, 4)), order='atom-major')
del(atoms[169])

# Setting the Calculator
orbff = pretrained.orb_v2(weights_path='/home/cgurwell/projects/rrg-ravh011/cgurwell/opt/orb-v2-20241011.ckpt', device='cuda') # or choose another model using ORB_PRETRAINED_MODELS[model_name]()
calculator = ORBCalculator(orbff, device='cuda')
atoms.calc = calculator

md = NVTBerendsen(
    atoms=atoms,
    temperature=float(sys.argv[2]),  # in K, set by slurm
    timestep=1*fs,  # in femto-seconds
    taut=0.5*1000*fs,
    trajectory=base + 'md_' + str(sys.argv[2]).replace('.', '_') + filename.replace('.cif', '.traj'),
    logfile=base + 'md_' + str(sys.argv[2]).replace('.', '_') + filename.replace('.cif', '.log'),
    loginterval=50,
)
md.run(50000)  # run an MD simulation