from pandas import read_table
import numpy as np

# Import lattice parameters
latt = read_table('MACE/elastic/LFVO/VASP/CONTCAR', sep='\s+', skiprows=2, nrows=3, header=None)
latt = latt.to_numpy()

# Import crystal coordinates
xyz = read_table('MACE/elastic/LFVO/VASP/CONTCAR', sep='\s+', skiprows=8, nrows=140, header=None)
xyz = xyz.to_numpy()

# Change to angstroms
for i in range(len(xyz)):
    xyz[i] = np.dot(latt, xyz[i])

# Set up atom indices
atms = ['Fe']*12
atms += ['V']*24
atms += ['O']*84
atms += ['Li']*20

atms = np.array(atms)

# Print atoms
print('\nAtoms:\n')
for i in range(len(atms)):
    print(atms[i], '\t', *xyz[i])

# Print lattice parameters
print('\nLattice Params:\n')
for i in range(len(latt)):
    print(*latt[i])



from ase import atoms
from ase.atoms import *
from ase.io import *

from ase.visualize import view

# Convert to CIF
atoms = Atoms(symbols=atms,
              positions=xyz,
              cell=latt,
              pbc=[1,1,1])
view(atoms)

write('LFVO_lithiated.cif', atoms)