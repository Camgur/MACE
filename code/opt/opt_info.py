from ase.io import read, Trajectory
import numpy as np
from mace.calculators import MACECalculator
import matplotlib.pyplot as plt

calculator = MACECalculator(model_paths=r"C:\Users\camgu\OneDrive\Documents\McMaster Archive\McMaster 2023-2024\Math Coding\Chem 4PB3\Resources\2024-01-07-mace-128-L2_epoch-199.model", device='cpu')
init_conf = read(r"C:\Users\camgu\OneDrive\Documents\McMaster Archive\McMaster 2023-2024\Math Coding\Chem 4PB3\Resources\Na4Sn2Ge5O16.cif")
opt_conf = read(r"C:\Users\camgu\Goward Group\Code\Ion_Channels\lammps\Na4Sn2Ge5O16_opt.cif")

init_conf.calc = calculator
opt_conf.calc = calculator

# print("Cell size before: ", init_conf.cell)
# print(init_conf.get_forces())
# print(init_conf.get_potential_energy())
# print("Cell size after: ", opt_conf.cell)
# print(opt_conf.get_forces())
# print(opt_conf.get_potential_energy())

