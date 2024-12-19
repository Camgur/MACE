import sys
import os

from ase import atoms
from ase.io import read
from ase.build import make_supercell
from ase.visualize import view

from chgnet.model.model import CHGNet
from chgnet.model.dynamics import MolecularDynamics
import warnings
warnings.filterwarnings("ignore", module="pymatgen")
warnings.filterwarnings("ignore", module="ase")

# Set File
file = 'MACE/asemd/LiAlO2_430184/LiAlO2_430184.cif'
filename = os.path.basename(file)
base = 'MACE/asemd/' + filename.replace('.cif', '') + '/chgnet/testing/'

# Importing CIF
atoms = read(file)
atoms = make_supercell(atoms, ((4, 0, 0), (0, 4, 0), (0, 0, 4)), order='atom-major')
del(atoms[169])
view(atoms)
assert 0


chgnet = CHGNet.load()

md = MolecularDynamics(
    atoms=atoms,
    model=chgnet,
    ensemble="nvt",
    temperature=298.15,  # in K, set by slurm
    timestep=1,  # in femto-seconds
    trajectory=base + 'md_' + filename.replace('.cif', '.traj'),
    logfile=base + 'md_' + filename.replace('.cif', '.log'),
    loginterval=100,
)
md.run(50000)  # run an MD simulation