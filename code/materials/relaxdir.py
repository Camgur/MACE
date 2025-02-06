import sys
import os

from chgnet.model.dynamics import CHGNetCalculator

from ase.optimize import BFGS

from ase import atoms
from ase.io import read, Trajectory

from ase.constraints import FixSymmetry
from ase.filters import FrechetCellFilter

# Set Dir
dir = str(input('Path to dir:\n'))

# Set text out
f = open(os.path.join(dir, 'energies.txt'), 'w')
f.close()
f = open(os.path.join(dir, 'energies.txt'), 'a')

# Save values
strings = []
energies = []

# Loop over files in Dir
for file in os.listdir(dir):
    if file.endswith('.cif'):
        file = os.path.join(dir, file)
        filename = os.path.basename(file)
        base = 'C:/Users/camgu/Goward/Code/MACE/materials/LAGP_263763/chgnet/'

        # Importing CIF
        atoms = read(file)

        # Setting the MACE-MP-0 Calculator
        calculator = CHGNetCalculator(use_device='cuda')
        atoms.calc = calculator

        # Preserve Unit Cell Symmetry
        atoms.set_constraint(FixSymmetry(atoms))

        # Run Optimise (Cell Opt) allow relaxation of unit cell
        # opt = BFGS(FrechetCellFilter(atoms))
        # opt.run(fmax=1e-5, steps=100)

        energy = atoms.get_total_energy()

        # Write atoms and energies
        # atoms.write(base + 'opt_' + filename)
        f.write(filename + '    ' + str(energy) + '\n')

        strings.append('opt_' + filename)
        energies.append(energy)

print('lowest energy: ', strings[energies.index(min(energies))])

f.close()

l = open(os.path.join(dir, 'energy_lowest.txt'), 'w')
l.write(strings[energies.index(min(energies))] + '  ' + str(min(energies)))
l.close()
