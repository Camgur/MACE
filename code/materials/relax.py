import sys
import os

import torch
torch.set_default_device('cuda')

from ase.optimize import BFGS

from ase import atoms
from ase.io import read

from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter

import warnings
warnings.simplefilter("ignore")

# Import Models
from chgnet.model.dynamics import CHGNetCalculator
# from matgl.models._m3gnet import M3GNet
# from matgl.apps.pes import Potential
# from matgl.ext.ase import M3GNetCalculator
from m3gnet.models import M3GNet, M3GNetCalculator, Potential
from mace.calculators import MACECalculator
from orb_models.forcefield import pretrained
from orb_models.forcefield.calculator import ORBCalculator



# Set File
file = r'espresso\lithium\LZPO_relax\LZPO_91112.cif'
filename = os.path.basename(file)
base = r'MACE\optimise\LZPO_91112/'


def chg():
    # Importing CIF
    atoms = read(file)

    # Setting the Calculator
    calculator = CHGNetCalculator(use_device='cuda')
    atoms.calc = calculator

    # Preserve Unit Cell Symmetry
    atoms.set_constraint(FixSymmetry(atoms))

    # Run Optimise (Cell Opt) allow relaxation of unit cell
    opt = BFGS(FrechetCellFilter(atoms), trajectory=base + '/chgnet/' + 'fullopt_' + filename.replace('.cif', '.traj'))
    opt.run(fmax=1e-5, steps=100)

    atoms.write(base + '/chgnet/' + 'fullopt_' + filename)

def m3g():
    # Importing CIF
    atoms = read(file)

    # Setting the Calculator
    mdl = M3GNet.load()
    calculator = M3GNetCalculator(potential=Potential(mdl))
    atoms.calc = calculator

    # Preserve Unit Cell Symmetry
    atoms.set_constraint(FixSymmetry(atoms))

    # Run Optimise (Cell Opt) allow relaxation of unit cell
    opt = BFGS(FrechetCellFilter(atoms), trajectory=base + '/m3gnet/' + 'fullopt_' + filename.replace('.cif', '.traj'))
    opt.run(fmax=1e-5, steps=100)

    atoms.write(base + '/m3gnet/' + 'fullopt_' + filename)

def mac():
    # Importing CIF
    atoms = read(file)

    # Setting the Calculator
    calculator = MACECalculator(model_paths=r'MACE\models\2024-01-07-mace-128-L2_epoch-199.model',
                                dispersion=False, device='cuda', default_dtype='float64')
    atoms.calc = calculator

    # Preserve Unit Cell Symmetry
    atoms.set_constraint(FixSymmetry(atoms))

    # Run Optimise (Cell Opt) allow relaxation of unit cell
    opt = BFGS(FrechetCellFilter(atoms), trajectory=base + '/mace/' + 'fullopt_' + filename.replace('.cif', '.traj'))
    opt.run(fmax=1e-5, steps=100)

    atoms.write(base + '/mace/' + 'fullopt_' + filename)

def orb():
    # Importing CIF
    atoms = read(file)

    # Setting the Calculator
    orbff = pretrained.orb_v2(weights_path='MACE\models\orb-v2-20241011.ckpt', device='cuda')
    calculator = ORBCalculator(orbff, device='cuda')
    atoms.calc = calculator

    # Preserve Unit Cell Symmetry
    atoms.set_constraint(FixSymmetry(atoms))

    # Run Optimise (Cell Opt) allow relaxation of unit cell
    opt = BFGS(FrechetCellFilter(atoms), trajectory=base + '/orb/' + 'fullopt_' + filename.replace('.cif', '.traj'))
    opt.run(fmax=1e-5, steps=100)

    atoms.write(base + '/orb/' + 'fullopt_' + filename)


chg()
# m3g() # Doesn't work with windows in this version (int64 error in find spherical points)
mac()
orb()