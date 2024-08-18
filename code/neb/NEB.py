from ase.io import read, Trajectory
from mace.calculators import MACECalculator
from ase.neb import NEB, DyNEB
from ase.optimize import BFGS
from ase.optimize import MDMin
from ase.visualize import view
# Read initial and final states:

calculator = MACECalculator(model_paths='/home/camgur/Documents/Coding/Chem_4PB3/Resources/2024-01-07-mace-128-L2_epoch-199.model', device='cuda', default_dtype='float64')
initial = read('/home/camgur/Documents/Coding/Goward/MACEMP0/Resources/Elastic/Na4Sn2Ge5O16_na2na3start.cif')
final = read('/home/camgur/Documents/Coding/Goward/MACEMP0/Resources/Elastic/Na4Sn2Ge5O16_na2na3end.cif')
# Make a band consisting of 5 images:
images = [initial]
images += [initial.copy() for i in range(3)]
images += [final]
neb = NEB(images, allow_shared_calculator=True)
# Interpolate linearly the potisions of the three middle images:
neb.interpolate()
# Set calculators:
for image in images[1:4]:
    image.calc = calculator
# Optimize:
optimizer = BFGS(neb, trajectory='Na22Na3.traj')
optimizer.run()

# for i in images:
#     view(i)