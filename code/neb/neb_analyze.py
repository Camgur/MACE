import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import matplotlib.pyplot as plt
import numpy as np
import os

from mace.calculators import MACECalculator
from chgnet.model.dynamics import CHGNetCalculator
from ase.visualize import view
from ase.io import read, Trajectory
from ase.mep import NEBTools

# images = read('/home/camgur/Documents/Coding/Na12Na1.traj@-5:')
file = 'MACE\elastic\LiAlO2\chgnet\LiAlO2_430184_chgnet_1to3.traj'
# file = 'MACE\elastic\LiAlO2\mace\LiAlO2_430184_mace_1to3.traj'
images = read(file + '@-12:')

# calculator = MACECalculator(model_paths='C:\\Users\\camgu\\Goward\\Code\\MACE\\models\\2024-01-07-mace-128-L2_epoch-199.model', 
#                             device='cuda', default_dtype='float64')
calculator = CHGNetCalculator(use_device='cuda')

for i in images:
    i.calc = calculator

nebtools = NEBTools(images)

# Get the barrier without any interpolation between highest images.
Ef, dE = nebtools.get_barrier(fit=False)

print(Ef, dE)

# Create a figure like that coming from ASE-GUI.
# fig = nebtools.plot_band()
# fig.savefig(file + '.png')

# view(images)

# plt.show()

line = np.linspace(0, 6, 12)

for n in images:
    print(n.get_total_energy())