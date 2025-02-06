from ase.io import read, Trajectory
import numpy as np
from mace.calculators import MACECalculator
import matplotlib.pyplot as plt

calculator = MACECalculator(model_paths=r"C:\Users\camgu\OneDrive\Documents\McMaster Archive\McMaster 2023-2024\Math Coding\Chem 4PB3\Resources\2024-01-07-mace-128-L2_epoch-199.model", device='cpu')


init_traj = Trajectory(r'C:\Users\camgu\OneDrive\Documents\McMaster Archive\McMaster 2023-2024\Math Coding\Chem 4PB3\Resources\Optimisation_Stuff\Optimisation_0_7.traj')

for traj in init_traj:
    descriptors = calculator.get_descriptors(init_traj[0])

    print(descriptors)
    desc = np.array(descriptors)
    print(desc.shape)

    # Plot the matrix
    plt.figure(figsize=(9, 5))
    plt.imshow(desc, cmap='hsv_r', interpolation='none', aspect='auto', vmin=-0.7, vmax=1.1)
    plt.colorbar()  # Optional: Adds a colorbar to interpret the values
    plt.title('Encoding Visualization')
    plt.xlabel('Tokens')
    plt.ylabel('Atom')
    plt.savefig()