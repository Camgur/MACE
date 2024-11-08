import warnings
warnings.simplefilter(action='ignore', category=FutureWarning)

import matplotlib.pyplot as plt
import os

from mace.calculators import MACECalculator
from ase.visualize import view
from ase.io import read, Trajectory
from ase.mep import NEBTools

# images = read('/home/camgur/Documents/Coding/Na12Na1.traj@-5:')
file = 'MACE\elastic\LiAlO2\mace\LiAlO2_430184_mace_1to3.traj'
images = read(file + '@-12:')

calculator = MACECalculator(model_paths='C:\\Users\\camgu\\Goward\\Code\\MACE\\2024-01-07-mace-128-L2_epoch-199.model', 
                            device='cuda', default_dtype='float64')

for i in images:
    i.calc = calculator

nebtools = NEBTools(images)

# Get the barrier without any interpolation between highest images.
Ef, dE = nebtools.get_barrier(fit=False)

print(Ef, dE)

# Create a figure like that coming from ASE-GUI.
fig = nebtools.plot_band()
fig.savefig(file + '.png')

view(images)

plt.show()