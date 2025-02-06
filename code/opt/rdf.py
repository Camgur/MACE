from ase.geometry.analysis import Analysis
from asetools.asetools.analysis.rdf import rdf
from ase.io import read, Trajectory
from ase.visualize import view

import numpy as np
import matplotlib.pyplot as plt


atoms = read('MACE\optimise\LTP_36777\chgnet\opt_LTP_36777.cif')
traj = Trajectory(r'MACE\asemd\LPSC_133976_0\chgnet\md_358_15_LPSC_133976_0.traj')

atoms = traj[0].copy()
atoms.wrap()

center = atoms.cell.diagonal()
atoms.set_positions(atoms.get_positions() - center)

# view(atoms)

g_r = rdf(traj, idx1="Li", idx2="Li")

x, y = zip(*g_r)

plt.plot(x, y)
plt.xlim([2,14])
plt.xlabel("$r$ / Å")
plt.ylabel("$g(r)$ / -")