import sys
import os

from ase import atoms
from ase.io import read

from chgnet.model.model import CHGNet
from chgnet.model.dynamics import MolecularDynamics
import warnings
warnings.filterwarnings("ignore", module="pymatgen")
warnings.filterwarnings("ignore", module="ase")

# Set File
file = 'MACE/asemd/LiFeV2O7_lith/LiFeV2O7_lith.cif'
filename = os.path.basename(file)
base = 'MACE/asemd/' + filename.replace('.cif', '') + '/chgnet/'

# Importing CIF
atoms = read(file)
atoms.edit()

chgnet = CHGNet.load()

md = MolecularDynamics(
    atoms=atoms,
    model=chgnet,
    ensemble="nvt",
    temperature=598.15,  # in K, set by slurm
    timestep=1,  # in femto-seconds
    trajectory=base + 'md_' + filename.replace('.cif', '.traj'),
    logfile=base + 'md_' + filename.replace('.cif', '.log'),
    loginterval=100,
)
md.run(50000)  # run an MD simulation