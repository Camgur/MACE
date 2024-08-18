import os
# import torch
import numpy as np
# import mace
import csv

from mace.calculators import MACECalculator
from ase.optimize import BFGS

from ase import atoms
from ase.io import *

from ase.constraints import ExpCellFilter
from ase.spacegroup.symmetrize import FixSymmetry
from ase.geometry.cell import *

# https://docs.matlantis.com/atomistic-simulation-tutorial/en/

'''
This code is intended to assess the lattice parameter optiisation
from MACE as a loss function, to return optimal parameters more
similar to the parent atomic system. Materials Project database
should be an optimal source of crystals, as they have been double-
refined, both in cell and atomic parameters.

Setup: Given a cell, optimise the geometry and return new cell
parameters as y_pred. Compare with old cell parameters (y) to
evaluate the loss function.

'''

# Define Simple Loss Function
def loss(atoms):

    return origin - cell_to_cellpar(atoms.cell)


# Define CSV Writer
def writer():
    with open(base + filename.replace('.cif', '.csv'), 'a', newline='') as f:
        writer = csv.writer(f, delimiter=',')
        writer.writerow(loss(atoms))
        f.close()
    # Attach write attribute to allow dyn.attach
    # THIS IS REALLY GROSS CODE, HELP
    data = loss(atoms)
    d = data
    data = Object()
    data.write = str(d)
    return data


# Set to object to allow attaching write in writer func
class Object(object):
    pass


# Import File
file = '/home/camgur/Documents/Coding/Goward/MACE/lattice/LiAlO2_430184.cif'
filename = os.path.basename(file)
base = '/home/camgur/Documents/Coding/Goward/MACE/lattice/'
with open(base + filename.replace('.cif', '.csv'), 'w') as f:
    wrt = csv.writer(f, delimiter=',')
    wrt.writerow(['a', 'b', 'c', 'alpha', 'beta', 'gamma'])
    f.close()

# Importing CIF
atoms = read(file)
atoms.calc = MACECalculator(model_paths='/home/camgur/Documents/Coding/Goward/MACE/2024-01-07-mace-128-L2_epoch-199.model',
                            dispersion=False, device='cuda', default_dtype='float64')
atoms.set_constraint(FixSymmetry(atoms))
origin = cell_to_cellpar(atoms.cell)


# Set Optimise (Atomic and Cell Params)
opt = BFGS(ExpCellFilter(atoms), trajectory=base + filename.replace('.cif', '.traj'))
opt.attach(writer)


'''
**Requires the object to have .write attribute for dyn.attach**
https://github.com/qsnake/ase/blob/master/ase/optimize/optimize.py

def attach(self, function, interval=1, *args, **kwargs):
    """Attach callback function.

    At every *interval* steps, call *function* with arguments
    *args* and keyword arguments *kwargs*."""

    if not hasattr(function, '__call__'):
        function = function.write
    self.observers.append((function, interval, args, kwargs))
'''


# Run Optimise
opt.run(fmax=1e-4, steps=50)
atoms.write(base + filename.replace('.cif', '_opt.cif'))

print('Finished Opt')



'''
class CellAwareBFGS(BFGS):
    def __init__(
        self,
        atoms: Atoms,
        restart: Optional[str] = None,
        logfile: Union[IO, str] = '-',
        trajectory: Optional[str] = None,
        append_trajectory: bool = False,
        maxstep: Optional[float] = None,
        bulk_modulus: Optional[float] = 145 * GPa,
        poisson_ratio: Optional[float] = 0.3,
        alpha: Optional[float] = None,
        long_output: Optional[bool] = False,
        **kwargs,
    ):
        self.bulk_modulus = bulk_modulus
        self.poisson_ratio = poisson_ratio
        self.long_output = long_output
        BFGS.__init__(self, atoms=atoms, restart=restart, logfile=logfile,
                      trajectory=trajectory, maxstep=maxstep,
                      alpha=alpha, append_trajectory=append_trajectory,
                      **kwargs)
        assert not isinstance(atoms, Atoms)
        if hasattr(atoms, 'exp_cell_factor'):
            assert atoms.exp_cell_factor == 1.0

    def initialize(self):
        BFGS.initialize(self)
        C_ijkl = calculate_isotropic_elasticity_tensor(
            self.bulk_modulus,
            self.poisson_ratio,
            suppress_rotation=self.alpha)
        cell_H = self.H0[-9:, -9:]
        ind = np.where(self.atoms.mask.ravel() != 0)[0]
        cell_H[np.ix_(ind, ind)] = C_ijkl.reshape((9, 9))[
            np.ix_(ind, ind)] * self.atoms.atoms.cell.volume

    def converged(self, forces=None):
        if forces is None:
            forces = self.atoms.atoms.get_forces()
        stress = self.atoms.atoms.get_stress()
        return np.max(np.sum(forces**2, axis=1))**0.5 < self.fmax and \
            np.max(np.abs(stress)) < self.smax

    def run(self, fmax=0.05, smax=0.005, steps=None):
        """ call Dynamics.run and keep track of fmax"""
        self.fmax = fmax
        self.smax = smax
        if steps is not None:
            self.max_steps = steps
        return Dynamics.run(self)

    def log(self, forces=None):
        if forces is None:
            forces = self.atoms.atoms.get_forces()
        fmax = (forces ** 2).sum(axis=1).max() ** 0.5
        e = self.optimizable.get_potential_energy()
        T = time.localtime()
        smax = abs(self.atoms.atoms.get_stress()).max()
        volume = self.atoms.atoms.cell.volume
        if self.logfile is not None:
            name = self.__class__.__name__
            if self.nsteps == 0:
                args = (" " * len(name),
                        "Step", "Time", "Energy", "fmax", "smax", "volume")
                msg = "\n%s  %4s %8s %15s  %15s %15s %15s" % args
                if self.long_output:
                    msg += ("%8s %8s %8s %8s %8s %8s" %
                            ('A', 'B', 'C', 'α', 'β', 'γ'))
                msg += '\n'
                self.logfile.write(msg)

            ast = ''
            args = (name, self.nsteps, T[3], T[4], T[5], e, ast, fmax, smax,
                    volume)
            msg = ("%s:  %3d %02d:%02d:%02d %15.6f%1s %15.6f %15.6f %15.6f" %
                   args)
            if self.long_output:
                msg += ("%8.3f %8.3f %8.3f %8.3f %8.3f %8.3f" %
                        tuple(cell_to_cellpar(self.atoms.atoms.cell)))
            msg += '\n'
            self.logfile.write(msg)

            self.logfile.flush()
'''