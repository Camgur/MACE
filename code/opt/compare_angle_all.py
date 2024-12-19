import numpy as np
import os
import pandas as pd

from ase import atoms
from ase.io import read

import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms
from ase.visualize import view

from ase.geometry import distance, analysis
from ase.neighborlist import build_neighbor_list, natural_cutoffs

# Define Structure
chgnet = 'MACE\optimise\LiFeV2O7\chgnet\opt_LiFeV2O7.cif'
m3gnet = 'MACE\optimise\LiFeV2O7\m3gnet\opt_LiFeV2O7.cif'
mace = 'MACE\optimise\LiFeV2O7\mace\opt_LiFeV2O7.cif'
orb = 'MACE\optimise\LiFeV2O7\orb\opt_LiFeV2O7.cif'

dft = 'MACE\optimise\LiFeV2O7/vasp\LiFeV2O7_vasp.cif'
exp = 'MACE\optimise\LiFeV2O7\LiFeV2O7.cif'
filepath = os.path.dirname(exp)

s1, s2, s3, s4, s5, s6 = read(chgnet), read(m3gnet), read(mace), read(orb), read(dft), read(exp)



# Define multiplier for bond distance
multiply = 1.1

# Bonds to find (separate elements by - and bonds by space e.g., Li-Fe-O V-Fe-O)
types = 'Li-Fe-O'
if ' ' in types:
    types = types.split(sep=' ')
    print('\nInput Bonds: ', types, '\n')
else:
    types = [types]
    print('\nOnly one bond found, ensure this is correct!\n', types, '\n')


# Compile the parts
compiled = [s1, s2, s3, s4, s5, s6]
strings = ['chgnet', 'm3gnet', 'mace', 'orb', 'dft', 'exp']
atoms = s1 + s2 + s3 + s4 + s5 + s6


'''
# Plot Atoms
fig, axarr = plt.subplots(1, 4, figsize=(15, 5))
plot_atoms(atoms, axarr[0], radii=0.7, rotation=('0x,0y,0z'))
plot_atoms(atoms, axarr[1], scale=0.7, offset=(3, 4), radii=0.3, rotation=('0x,0y,0z'))
plot_atoms(atoms, axarr[2], radii=0.7, rotation=('45x,45y,0z'))
plot_atoms(atoms, axarr[3], radii=0.7, rotation=('0x,0y,0z'))
axarr[0].set_title("No rotation")
axarr[1].set_xlabel("X-axis, [$\mathrm{\AA}$]")
axarr[1].set_ylabel("Y-axis, [$\mathrm{\AA}$]")
axarr[2].set_axis_off()
axarr[3].set_xlim(2, 6)
axarr[3].set_ylim(2, 6)

plt.show()
'''

compilation1 = np.zeros((len(types), 6, 1000))
compilation2 = np.zeros((len(types), 5, 1000))




# Run Compared to Experimental
print('\n\nEXP\n')

i=0
# Loop over all bonds provided
for type in types:
    print(type, '\n')
    type = type.split('-')
    n = 0

    for structure, string in zip(compiled, strings):
        total_diff = distance(s6, structure, permute=False)
        print('\n' + string, ' total distance mismatch (A): ', total_diff)

        analyse = analysis.Analysis(s6, build_neighbor_list(s6, cutoffs=natural_cutoffs(s6, mult=multiply)))
        analyse2 = analysis.Analysis(structure, build_neighbor_list(structure, cutoffs=natural_cutoffs(structure, mult=multiply)))
        bonds = analyse.get_angles(type[0], type[1], type[2], unique=True)
        bonds2 = analyse2.get_angles(type[0], type[1], type[2], unique=True)
        try:
            bonds_exp = np.array(analyse.get_values(bonds)[0])
            bonds_struct = np.array(analyse2.get_values(bonds2)[0])
        except:
            pass

        try:
            bond_diff = np.abs(bonds_exp - bonds_struct)
        except:
            print('Failed to calculate bond for ' + string)
            bond_diff = [0]

        compilation1[i, n, 0:len(bond_diff)] = bond_diff
        n += 1

    i += 1

# Repack for excel
# names must equal the number of dimensions (i.e., three for 3D)
names = ['x', 'y', 'z']

# Set number of bonds by shape
ranged = list(range(compilation1.shape[2]))

# Build MultiIndex and flatten to index
index = pd.MultiIndex.from_product([types, strings, ranged], names=names)
df = pd.DataFrame({'A': compilation1.flatten()}, index=index)['A']

# Resort the stack, apply label
df = df.unstack(level='x').swaplevel().sort_index()
df = df.unstack(level='y').sort_index()
df.index.names = [None]
df.columns.names = ['Type', 'Model']

# Replace Zeros with NaN
df.replace(0, np.nan, inplace=True)

# Export to excel
df.to_excel(filepath + '/exp_angles.xlsx', index=True, header=True)





# Run Compared to DFT
print('\n\nDFT\n')

i=0
# Loop over all bonds provided
for type in types:
    print(type, '\n')
    type = type.split('-')
    n = 0

    for structure, string in zip(compiled[:5], strings[:5]):
        total_diff = distance(s5, structure, permute=False)
        print('\n' + string, ' total distance mismatch (A): ', total_diff)

        analyse = analysis.Analysis(s5, build_neighbor_list(s5, cutoffs=natural_cutoffs(s5, mult=multiply)))
        analyse2 = analysis.Analysis(structure, build_neighbor_list(structure, cutoffs=natural_cutoffs(structure, mult=multiply)))
        bonds = analyse.get_angles(type[0], type[1], type[2], unique=True)
        bonds2 = analyse2.get_angles(type[0], type[1], type[2], unique=True)
        try:
            bonds_exp = np.array(analyse.get_values(bonds)[0])
            bonds_struct = np.array(analyse2.get_values(bonds2)[0])
        except:
            pass

        try:
            bond_diff = np.abs(bonds_exp - bonds_struct)
        except:
            print('Failed to calculate bond for ' + string)
            bond_diff = [0]

        compilation2[i, n, 0:len(bond_diff)] = bond_diff
        n += 1

    i += 1

# Repack for excel
# names must equal the number of dimensions (i.e., three for 3D)
names = ['x', 'y', 'z']

# Set number of bonds by shape
ranged = list(range(compilation2.shape[2]))

# Build MultiIndex and flatten to index
index = pd.MultiIndex.from_product([types, strings[:5], ranged], names=names)
df = pd.DataFrame({'A': compilation2.flatten()}, index=index)['A']

# Resort the stack, apply label
df = df.unstack(level='x').swaplevel().sort_index()
df = df.unstack(level='y').sort_index()
df.index.names = [None]
df.columns.names = ['Type', 'Model']

# Replace Zeros with NaN
df.replace(0, np.nan, inplace=True)

# Export to excel
df.to_excel(filepath + '/dft_angles.xlsx', index=True, header=True)
