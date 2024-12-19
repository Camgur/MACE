import sys
import os

from ase import atoms
from ase.io import read
from ase.build import make_supercell

from chgnet.model.model import CHGNet
from chgnet.model.dynamics import MolecularDynamics
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

chgnet = CHGNet.load()

md = MolecularDynamics(
    atoms=atoms,
    model=chgnet,
    ensemble="nvt",
    temperature=float(sys.argv[2]),  # in K, set by slurm
    timestep=1,  # in femto-seconds
    trajectory=base + 'md_' + str(sys.argv[2]).replace('.', '_') + '_' + filename.replace('.cif', '.traj'),
    logfile=base + 'md_' + str(sys.argv[2]).replace('.', '_') + '_' + filename.replace('.cif', '.log'),
    loginterval=50,
)
md.run(50000)  # run an MD simulation