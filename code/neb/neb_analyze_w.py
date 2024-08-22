import matplotlib.pyplot as plt

from mace.calculators import MACECalculator
from ase.io import read, Trajectory
from ase.neb import NEBTools

# images = read('/home/camgur/Documents/Coding/Na12Na1.traj@-5:')
images = read('MACE\\elastic\\LiAlO2\\neb.traj@-7:')

calculator = MACECalculator(model_paths='C:\\Users\\camgu\\Goward\\Code\\MACE\\2024-01-07-mace-128-L2_epoch-199.model', 
                            device='cpu', default_dtype='float32')

for i in images:
    i.calc = calculator

nebtools = NEBTools(images)

# Get the barrier without any interpolation between highest images.
Ef, dE = nebtools.get_barrier(fit=False)

print(Ef, dE)

# Create a figure like that coming from ASE-GUI.
nebtools.plot_band()
# fig.savefig('diffusion-barrier.png')

plt.show()