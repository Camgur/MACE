from ase.io import read, Trajectory
from mace.calculators import MACECalculator
from ase.neb import NEB, DyNEB
from ase.constraints import FixAtoms
from ase.optimize import BFGS
from ase.optimize import MDMin
from ase.visualize import view
# Read initial and final states:

calculator = MACECalculator(model_paths='/home/camgur/Documents/Coding/Chem_4PB3/Resources/2024-01-07-mace-128-L2_epoch-199.model', device='cuda', default_dtype='float64')
initial = read('/home/camgur/Documents/Coding/Goward/MACEMP0/Resources/Elastic/Na4Sn2Ge5O16_na2na3start.cif')
final = read('/home/camgur/Documents/Coding/Goward/MACEMP0/Resources/Elastic/Na4Sn2Ge5O16_na2na3end.cif')

# Set Constraint
# constraint = FixAtoms(mask=[atom.index != 29 for atom in initial]) # For Na1 to Na2 and Na3
constraint = FixAtoms(mask=[atom.index != 39 for atom in initial]) # For Na2 to Na3

# Make a band consisting of 5 images:
images = [initial]
for i in range(3):
    image = initial.copy()
    image.calc = calculator
    image.set_constraint(constraint)
    images.append(image)


images.append(final)


neb = NEB(images, allow_shared_calculator=True)

# Interpolate linearly the potisions of the middle images:
neb.interpolate()

# Optimize:
optimizer = BFGS(neb, trajectory='Na22Na3.traj')
optimizer.run(fmax=0.05)

# for i in images:
#     view(i)