import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.linear_model import LinearRegression
from ase import io, atoms
from ase.geometry import rdf


chgnet = []
m3gnet = []
mace = []
orb = []

dir1 = os.listdir('MACE/materials/for_trj/chgnet/600/')
dir2 = os.listdir('MACE/materials/for_trj/m3gnet/600/')
dir3 = os.listdir('MACE/materials/for_trj/mace/600/')
dir4 = os.listdir('MACE/materials/for_trj/orb/600/')

for item in dir1:
    chgnet.append(io.read('MACE/materials/for_trj/chgnet/600/' + item, index='-1'))
for item in dir2:
    m3gnet.append(io.read('MACE/materials/for_trj/m3gnet/600/' + item, index='-1'))
for item in dir3:
    mace.append(io.read('MACE/materials/for_trj/mace/600/' + item, index='-1'))
for item in dir4:
    orb.append(io.read('MACE/materials/for_trj/orb/600/' + item, index='-1'))



c = []
m3 = []
m = []
o = []

radii = [7.0, 8, 8]
for i in range(len(chgnet)):
    c.append(rdf.get_rdf(chgnet[i], radii[i], nbins=100))
    m3.append(rdf.get_rdf(m3gnet[i], radii[i], nbins=100))
    m.append(rdf.get_rdf(mace[i], radii[i], nbins=100))
    o.append(rdf.get_rdf(orb[i], radii[i], nbins=100))
    print(i)





# Create a set of subplots in a single column with seven subplots
fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)

# Define different markers and colors for each point
materials = ['LAGP', 'LGPS', 'LSnPS']

# Loop through each subplot and create a number line
for i, ax in enumerate(axes):

    # Plot different markers
    ax.plot(c[i][1], c[i][0], label='chgnet', color='Blue', linestyle='solid')
    ax.plot(m3[i][1], m3[i][0], label='m3gnet', color='Purple', linestyle='dashed')
    ax.plot(m[i][1], m[i][0], label='mace', color='Red', linestyle='dotted')
    ax.plot(o[i][1], o[i][0], label='orb', color='Orange', linestyle='dashdot')

    # Customize the appearance
    ax.set_ylabel(materials[i], rotation=0, labelpad=30, fontsize=16)
    ax.set_yticks([])
    ax.grid(False)  # Remove gridlines

    # Remove borders (spines) around each subplot
    # ax.spines['top'].set_visible(False)
    # ax.spines['right'].set_visible(False)
    # ax.spines['left'].set_visible(False)
    # ax.spines['bottom'].set_visible(False)

# Adjust layout to further decrease space between subplots
# plt.tight_layout(rect=[0, 0, 0, 0])
plt.xlabel('Radial Distance [Å]', fontsize=16)
# plt.subplots_adjust(hspace=0)
plt.legend()

# Show the plot
plt.savefig('MACE/figures/md_rdf.png', dpi=260)
plt.savefig('MACE/figures/md_rdf.svg')
plt.show()