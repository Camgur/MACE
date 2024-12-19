import numpy as np
import pandas as pd
from ase import atoms
from ase.io import read

import matplotlib.pyplot as plt
from ase.visualize.plot import plot_atoms
from ase.visualize import view

from ase.geometry import get_distances, distance, analysis
from ase.neighborlist import NeighborList,natural_cutoffs,build_neighbor_list,get_distance_indices,get_distance_matrix, get_connectivity_matrix


'''
# LiAlO2
chgnet = read('MACE/optimise/LiAlO2_430184/chgnet/opt_LiAlO2_430184.cif')
m3gnet = read('MACE/optimise/LiAlO2_430184/m3gnet/opt_LiAlO2_430184.cif')
mace = read('MACE/optimise/LiAlO2_430184/mace/opt_LiAlO2_430184.cif')
orb = read('MACE/optimise/LiAlO2_430184/orb/opt_LiAlO2_430184.cif')

dft = read('MACE/optimise/LiAlO2_430184/qe/LiAlO2_qe_opt.cif')

exp = read('MACE/optimise/LiAlO2_430184/LiAlO2_430184.cif')
'''


# LAC
chgnet = read('MACE/optimise/LAC_35275/chgnet/opt_LAC_35275.cif')
m3gnet = read('MACE/optimise/LAC_35275/m3gnet/opt_LAC_35275.cif')
mace = read('MACE/optimise/LAC_35275/mace/opt_LAC_35275.cif')
orb = read('MACE/optimise/LAC_35275/orb/opt_LAC_35275.cif')

dft = read('MACE/optimise/LAC_35275/qe/LAC_qe_opt.cif')

exp = read('MACE/optimise/LAC_35275/LAC_35275.cif')


'''
# LZPO
chgnet = read('MACE/optimise/LZPO_91112/chgnet/opt_LZPO_91112.cif')
m3gnet = read('MACE/optimise/LZPO_91112/m3gnet/opt_LZPO_91112.cif')
mace = read('MACE/optimise/LZPO_91112/mace/opt_LZPO_91112.cif')
orb = read('MACE/optimise/LZPO_91112/orb/opt_LZPO_91112.cif')

dft = read('MACE/optimise/LZPO_91112/qe/LZPO_qe_opt.cif')

exp = read('MACE/optimise/LZPO_91112/LZPO_91112.cif')
'''

# Compile
compiled = [chgnet, m3gnet, mace, orb, dft, exp]
strings = ['chgnet', 'm3gnet', 'mace', 'orb', 'dft', 'exp']
atoms = chgnet + m3gnet + mace + orb + dft + exp


'''
# Plot
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
i=0

compilation = []
compilation2 = []

'''
# Difference (Li-O)
for structure, string in zip(compiled, strings):
    total_diff = distance(exp, structure, permute=False)
    print('Total distance mismatch (A): ', total_diff)

    analyse = analysis.Analysis(exp, build_neighbor_list(exp))
    analyse2 = analysis.Analysis(structure, build_neighbor_list(structure))
    bonds = analyse.get_bonds('Li', 'O', unique=True)
    bonds2 = analyse2.get_bonds('Li', 'O', unique=True)

    bonds_exp = np.array(analyse.get_values(bonds)[0])
    bonds_struct = np.array(analyse2.get_values(bonds2)[0])

    bond_diff = np.abs(bonds_exp - bonds_struct)
    # print(string, 'Li-O bond difference: ', bond_diff, '\n')

    compilation.append(bond_diff)
i+=1
print('\n')

# Difference (Al-O)
for structure, string in zip(compiled, strings):
    total_diff = distance(exp, structure, permute=False)
    print('Total distance mismatch (A): ', total_diff)

    analyse = analysis.Analysis(exp, build_neighbor_list(exp))
    analyse2 = analysis.Analysis(structure, build_neighbor_list(structure))
    bonds = analyse.get_bonds('Al', 'O', unique=True)
    bonds2 = analyse2.get_bonds('Al', 'O', unique=True)

    bonds_exp = np.array(analyse.get_values(bonds)[0])
    bonds_struct = np.array(analyse2.get_values(bonds2)[0])

    bond_diff = np.abs(bonds_exp - bonds_struct)
    # print(string, 'Al-O bond difference: ', bond_diff, '\n')

    compilation.append(bond_diff)
i+=1
print('\n')
'''
'''
# Difference (Li-Cl)
for structure, string in zip(compiled, strings):
    total_diff = distance(exp, structure, permute=False)
    print('Total distance mismatch (A): ', total_diff)

    analyse = analysis.Analysis(exp, build_neighbor_list(exp, cutoffs=natural_cutoffs(exp, mult=1.1)))
    analyse2 = analysis.Analysis(structure, build_neighbor_list(structure, cutoffs=natural_cutoffs(exp, mult=1.1)))
    bonds = analyse.get_bonds('Li', 'Cl', unique=True)
    bonds2 = analyse2.get_bonds('Li', 'Cl', unique=True)

    bonds_exp = np.array(analyse.get_values(bonds)[0])
    bonds_struct = np.array(analyse2.get_values(bonds2)[0])

    bond_diff = np.abs(bonds_exp - bonds_struct)
    # print(string, 'Li-Cl bond difference: ', bond_diff, '\n')

    compilation.append(bond_diff)
i+=1
print('\n')

# Difference (Al-Cl)
for structure, string in zip(compiled, strings):
    total_diff = distance(exp, structure, permute=False)
    print('Total distance mismatch (A): ', total_diff)

    analyse = analysis.Analysis(exp, build_neighbor_list(exp))
    analyse2 = analysis.Analysis(structure, build_neighbor_list(structure))
    bonds = analyse.get_bonds('Al', 'Cl', unique=True)
    bonds2 = analyse2.get_bonds('Al', 'Cl', unique=True)

    bonds_exp = np.array(analyse.get_values(bonds)[0])
    bonds_struct = np.array(analyse2.get_values(bonds2)[0])

    bond_diff = np.abs(bonds_exp - bonds_struct)
    # print(string, 'Li-Cl bond difference: ', bond_diff, '\n')

    compilation2.append(bond_diff)
i+=1
print('\n')

compilation = np.array(compilation)
compilation1 = np.array(compilation2)

df = pd.DataFrame(compilation[0:6], index=strings)
df.to_excel('MACE/optimise/LAC_35275/li-cl_distances.xlsx', index=True)

df = pd.DataFrame(compilation2, index=strings)
df.to_excel('MACE/optimise/LAC_35275/al-cl_distances.xlsx', index=True)
'''






'''
# Difference (Li-O) DFT
for structure, string in zip(compiled[:5], strings[:5]):
    total_diff = distance(dft, structure, permute=False)
    print('Total distance mismatch (A): ', total_diff)

    analyse = analysis.Analysis(dft, build_neighbor_list(dft))
    analyse2 = analysis.Analysis(structure, build_neighbor_list(structure))
    bonds = analyse.get_bonds('Li', 'O', unique=True)
    bonds2 = analyse2.get_bonds('Li', 'O', unique=True)

    bonds_exp = np.array(analyse.get_values(bonds)[0])
    bonds_struct = np.array(analyse2.get_values(bonds2)[0])

    bond_diff = np.abs(bonds_exp - bonds_struct)
    # print(string, 'Li-O bond difference: ', bond_diff, '\n')

    compilation.append(bond_diff)

print('\n')

# Difference (Al-O) DFT
for structure, string in zip(compiled[:5], strings[:5]):
    total_diff = distance(dft, structure, permute=False)
    print('Total distance mismatch (A): ', total_diff)

    analyse = analysis.Analysis(dft, build_neighbor_list(dft))
    analyse2 = analysis.Analysis(structure, build_neighbor_list(structure))
    bonds = analyse.get_bonds('Al', 'O', unique=True)
    bonds2 = analyse2.get_bonds('Al', 'O', unique=True)

    bonds_exp = np.array(analyse.get_values(bonds)[0])
    bonds_struct = np.array(analyse2.get_values(bonds2)[0])

    bond_diff = np.abs(bonds_exp - bonds_struct)
    # print(string, 'Al-O bond difference: ', bond_diff, '\n')

    compilation.append(bond_diff)
'''
    

# Difference (Li-Cl) DFT
for structure, string in zip(compiled[:5], strings[:5]):
    total_diff = distance(dft, structure, permute=False)
    print('Total distance mismatch (A): ', total_diff)

    analyse = analysis.Analysis(dft, build_neighbor_list(dft, cutoffs=natural_cutoffs(exp, mult=1.1)))
    analyse2 = analysis.Analysis(structure, build_neighbor_list(structure, cutoffs=natural_cutoffs(exp, mult=1.1)))
    bonds = analyse.get_bonds('Li', 'Cl', unique=True)
    bonds2 = analyse2.get_bonds('Li', 'Cl', unique=True)

    bonds_exp = np.array(analyse.get_values(bonds)[0])
    bonds_struct = np.array(analyse2.get_values(bonds2)[0])

    bond_diff = np.abs(bonds_exp - bonds_struct)
    # print(string, 'Li-Cl bond difference: ', bond_diff, '\n')

    compilation.append(bond_diff)
i+=1
print('\n')

# Difference (Al-Cl) DFT
for structure, string in zip(compiled[:5], strings[:5]):
    total_diff = distance(dft, structure, permute=False)
    print('Total distance mismatch (A): ', total_diff)

    analyse = analysis.Analysis(dft, build_neighbor_list(exp))
    analyse2 = analysis.Analysis(structure, build_neighbor_list(structure))
    bonds = analyse.get_bonds('Al', 'Cl', unique=True)
    bonds2 = analyse2.get_bonds('Al', 'Cl', unique=True)

    bonds_exp = np.array(analyse.get_values(bonds)[0])
    bonds_struct = np.array(analyse2.get_values(bonds2)[0])

    bond_diff = np.abs(bonds_exp - bonds_struct)
    # print(string, 'Li-Cl bond difference: ', bond_diff, '\n')

    compilation2.append(bond_diff)
i+=1
print('\n')



compilation = np.array(compilation)
compilation2 = np.array(compilation2)

df = pd.DataFrame(compilation[0:5], index=strings[:5])
df.to_excel('MACE/optimise/LAC_35275/dftli-cl_distances.xlsx', index=True)

df = pd.DataFrame(compilation2, index=strings[:5])
df.to_excel('MACE/optimise/LAC_35275/dftal-cl_distances.xlsx', index=True)
