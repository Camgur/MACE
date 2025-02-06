import numpy as np
import os
import sys
import pandas as pd
from ase import atoms
from ase.io import read

import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms
from ase.visualize import view

from ase.geometry import get_distances, distance, analysis
from ase.neighborlist import NeighborList,natural_cutoffs,build_neighbor_list,get_distance_indices,get_distance_matrix, get_connectivity_matrix

# Define Structure
chgnet = 'MACE\optimise\LTP_36777\chgnet\opt_LTP_36777.cif'
m3gnet = 'MACE\optimise\LTP_36777\m3gnet\opt_LTP_36777.cif'
mace = 'MACE\optimise\LTP_36777\mace\opt_LTP_36777.cif'
orb = 'MACE\optimise\LTP_36777\orb\opt_LTP_36777.cif'

dft = 'MACE\optimise\LTP_36777\qe\LTP_qe_opt.cif'
exp = 'MACE\optimise\LTP_36777\LTP_36777.cif'
filepath = os.path.dirname(exp)

s1, s2, s3, s4, s5, s6 = read(chgnet), read(m3gnet), read(mace), read(orb), read(dft), read(exp)

# Define multiplier for bond distance
multiply1 = 1.0
multiply2 = 1.0


# Bonds to find (separate elements by - and bonds by space e.g., Li-Fe Fe-O Li-O)
types = 'Ti-O Li-O P-O'
if ' ' in types:
    types = types.split(sep=' ')
    print('\nInput Bonds: ', types, '\n')
else:
    types = [types]
    print('\nOnly one bond found, ensure this is correct!\n', types, '\n')


# Compile the parts
compiled = [s1, s2, s3, s4, s5, s6]
strings = ['chgnet', 'm3gnet', 'mace', 'orb', 'dft', 'exp']





'''
# For generating plots
compiled2 = [s1, s2, s3, s4, s5, s6]
atoms = s1 + s2 + s3 + s4 + s5 + s6

# Change active number of colours
mol = [len(comp) for comp in compiled2]
prec = np.linspace(0, 1, len(mol))


numbers = [ele for ele in prec  for i in range(mol[0])]

from matplotlib import colormaps
map = colormaps.get_cmap('rainbow')
colours = [map(num) for num in numbers]

# Plot Atoms
fig, axarr = plt.subplots(1, 3, figsize=(15, 5))
plot_atoms(atoms, axarr[0], radii=0.7, rotation=('0x,0y,0z'), colors = colours)
# plot_atoms(atoms, axarr[1], scale=0.7, offset=(3, 4), radii=0.3, rotation=('0x,0y,0z'), colors = colours)
plot_atoms(atoms, axarr[1], radii=0.7, rotation=('45x,45y,0z'), colors = colours)
plot_atoms(atoms, axarr[2], radii=0.7, rotation=('0x,0y,0z'), colors = colours)
axarr[0].set_title("No rotation")
# axarr[1].set_xlabel("X-axis, [$\mathrm{\AA}$]")
# axarr[1].set_ylabel("Y-axis, [$\mathrm{\AA}$]")
axarr[1].set_axis_off()
axarr[2].set_xlim(6, 10)
axarr[2].set_ylim(6, 10)

plt.show()

assert 0
'''






compilation1 = np.zeros((len(types), 6, 150))
compilation2 = np.zeros((len(types), 5, 150))


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
        param = np.abs(s6.cell.cellpar() - structure.cell.cellpar())
        print('\n' + string, ' total distance mismatch (A): ', total_diff)
        if np.sum(param) != float(0):
            print(string, ' total cell mismatch (A, degrees): ', param)

        analyse = analysis.Analysis(s6, build_neighbor_list(s6, cutoffs=natural_cutoffs(s6, mult=multiply1)))
        analyse2 = analysis.Analysis(structure, build_neighbor_list(structure, cutoffs=natural_cutoffs(structure, mult=multiply2)))
        bonds = analyse.get_bonds(type[0], type[1], unique=True)
        bonds2 = analyse2.get_bonds(type[0], type[1], unique=True)

        bonds_exp = np.array(analyse.get_values(bonds)[0])
        bonds_struct = np.array(analyse2.get_values(bonds2)[0])

        try:
            bond_diff = np.abs(bonds_exp - bonds_struct)
        except:
            print('Failed to calculate bond for ' + string)
            print('No broadcast: ', len(bonds_exp), len(bonds_struct))
            bond_diff = [0, 0]

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
df.to_excel(filepath + '/exp_distances.xlsx', index=True, header=True)





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
        param = np.abs(s5.cell.cellpar() - structure.cell.cellpar())
        print('\n' + string, ' total distance mismatch (A): ', total_diff)
        if np.sum(param) != float(0):
            print(string, ' total cell mismatch (A, degrees): ', param)

        analyse = analysis.Analysis(s5, build_neighbor_list(s5, cutoffs=natural_cutoffs(s5, mult=multiply1)))
        analyse2 = analysis.Analysis(structure, build_neighbor_list(structure, cutoffs=natural_cutoffs(structure, mult=multiply2)))
        bonds = analyse.get_bonds(type[0], type[1], unique=True)
        bonds2 = analyse2.get_bonds(type[0], type[1], unique=True)

        bonds_exp = np.array(analyse.get_values(bonds)[0])
        bonds_struct = np.array(analyse2.get_values(bonds2)[0])

        try:
            bond_diff = np.abs(bonds_exp - bonds_struct)
        except:
            print('Failed to calculate bond for ' + string)
            print('No broadcast: ', len(bonds_exp), len(bonds_struct))
            bond_diff = [0, 0]

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
df.to_excel(filepath + '/dft_distances.xlsx', index=True, header=True)
