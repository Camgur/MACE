import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from sklearn.linear_model import LinearRegression
from ase import io, atoms


'''
chgnet = []
m3gnet = []
mace = []
orb = []
dft = []
exp = []

dir1 = os.listdir('MACE/materials/for_compare/chgnet/')
dir2 = os.listdir('MACE/materials/for_compare/m3gnet/')
dir3 = os.listdir('MACE/materials/for_compare/mace/')
dir4 = os.listdir('MACE/materials/for_compare/orb/')
dir5 = os.listdir('MACE/materials/for_compare/dft/')
dir6 = os.listdir('MACE/materials/for_compare/exp/')

for item in dir1:
    chgnet.append(io.read('MACE/materials/for_compare/chgnet/' + item))
for item in dir2:
    m3gnet.append(io.read('MACE/materials/for_compare/m3gnet/' + item))
for item in dir3:
    mace.append(io.read('MACE/materials/for_compare/mace/' + item))
for item in dir4:
    orb.append(io.read('MACE/materials/for_compare/orb/' + item))
for item in dir5:
    dft.append(io.read('MACE/materials/for_compare/dft/' + item))
for item in dir6:
    exp.append(io.read('MACE/materials/for_compare/exp/' + item))
    print(item)


def expansion(file, expt):



    # Get volumes from object
    v1 = file.get_volume()
    v2 = expt.get_volume()

    # print(v1, v2)
    return ((v1/v2) - 1) * 100

c = []
m3 = []
m = []
o = []
d = []

for i in range(len(exp)):
    c.append(expansion(chgnet[i], exp[i]))
    m3.append(expansion(m3gnet[i], exp[i]))
    m.append(expansion(mace[i], exp[i]))
    o.append(expansion(orb[i], exp[i]))
    d.append(expansion(dft[i], exp[i]))
print(m)
data = {
    'CHGNet' : c,
    'M3GNet' : m3,
    'MACE' : m,
    'ORB' : o,
    'DFT' : d
}
'''
'''
# Create a set of subplots in a single column with seven subplots
fig, axes = plt.subplots(nrows=7, ncols=1, figsize=[8,6], sharex=True)

# Define different markers and colors for each point
materials = ['LAC', 'LGP', 'LiAlO2', 'LFVO', 'LFVO_L', 'LTP', 'LZPO']

# Loop through each subplot and create a number line
for i, ax in enumerate(axes):

    # Plot different markers
    ax.scatter(d[i], 0, label='dft', color='Turquoise', marker='h', s=60)
    ax.scatter(c[i], 0, label='chgnet', color='Blue', marker='o', s=60)
    # ax.scatter(m3[i], 0, label='m3gnet', color='Purple', marker='v', s=60)
    ax.scatter(m[i], 0, label='mace', color='Red', marker='s', s=60)
    ax.scatter(o[i], 0, label='orb', color='Orange', marker='D', s=60)

    # Customize the appearance
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_ylabel(materials[i], fontsize=14, rotation=0, labelpad=30)
    ax.grid(False)  # Remove gridlines

    # Remove borders (spines) around each subplot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

    ax.tick_params(axis='x', labelsize=14)

# Adjust layout to further decrease space between subplots
plt.tight_layout(rect=[0, 0, 0, 0])
plt.xlabel('Volume Expansion [%]', fontsize=16)
plt.subplots_adjust(hspace=0)
plt.legend(loc='upper right', bbox_to_anchor=(1.1, 2), fontsize=12)

# Show the plot
plt.savefig('MACE/figures/candidate_volume_2_no_m3_grd.png')
plt.savefig('MACE/figures/candidate_volume_2_no_m3_grd.svg')
plt.show()
'''



'''
# Create a set of subplots in a single column with seven subplots
fig, axes = plt.subplots(nrows=7, ncols=1, figsize=[8,6], sharex=True)

# Define different markers and colors for each point
materials = ['LAC', 'LGP', 'LiAlO2', 'LFVO', 'LFVO_L', 'LTP', 'LZPO']

# Loop through each subplot and create a number line
for i, ax in enumerate(axes):

    # Plot different markers
    ax.scatter(d[i], 0, label='dft', color='Turquoise', marker='h', s=60)
    ax.scatter(c[i], 0, label='chgnet', color='Blue', marker='o', s=60)
    ax.scatter(m3[i], 0, label='m3gnet', color='Purple', marker='v', s=60)
    ax.scatter(m[i], 0, label='mace', color='Red', marker='s', s=60)
    ax.scatter(o[i], 0, label='orb', color='Orange', marker='D', s=60)

    # Customize the appearance
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_ylabel(materials[i], fontsize=10, rotation=0)
    ax.grid(True)  # Remove gridlines

    # Remove borders (spines) around each subplot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

# Adjust layout to further decrease space between subplots
plt.tight_layout(rect=[0, 0, 0, 0])
plt.xlabel('Volume Expansion [%]', fontsize=16)
plt.subplots_adjust(hspace=0)
plt.legend()

# Show the plot
plt.savefig('MACE/figures/candidate_volume_2.png')
plt.savefig('MACE/figures/candidate_volume_2.svg')
plt.show()
'''

'''
# Convert to pandas
df = pd.DataFrame(data)

colours = ['Blue', 'Purple', 'Red', 'Orange', 'Black']

# Begin plot
sns.boxplot(data=df, orient='h', palette=colours)

plt.xlabel('Volume Expansion [%]', fontsize=16)
plt.savefig('MACE/figures/candidate_volume.png')
plt.savefig('MACE/figures/candidate_volume.svg')
plt.show()

'''


chgnet = []
m3gnet = []
mace = []
orb = []
dft = []
exp = []

dir1 = os.listdir('MACE/materials/for_md/chgnet/')
dir2 = os.listdir('MACE/materials/for_md/m3gnet/')
dir3 = os.listdir('MACE/materials/for_md/mace/')
dir4 = os.listdir('MACE/materials/for_md/orb/')
dir6 = os.listdir('MACE/materials/for_md/exp/')

for item in dir1:
    chgnet.append(io.read('MACE/materials/for_md/chgnet/' + item))
for item in dir2:
    m3gnet.append(io.read('MACE/materials/for_md/m3gnet/' + item))
for item in dir3:
    mace.append(io.read('MACE/materials/for_md/mace/' + item))
for item in dir4:
    orb.append(io.read('MACE/materials/for_md/orb/' + item))
for item in dir6:
    exp.append(io.read('MACE/materials/for_md/exp/' + item))
    print(item)


def expansion(file, expt):



    # Get volumes from object
    v1 = file.get_volume()
    v2 = expt.get_volume()

    # print(v1, v2)
    return ((v1/v2) - 1) * 100

c = []
m3 = []
m = []
o = []

for i in range(len(exp)):
    c.append(expansion(chgnet[i], exp[i]))
    m3.append(expansion(m3gnet[i], exp[i]))
    m.append(expansion(mace[i], exp[i]))
    o.append(expansion(orb[i], exp[i]))

'''
data = {
    'CHGNet' : c,
    'M3GNet' : m3,
    'MACE' : m,
    'ORB' : o,
}

# Convert to pandas
df = pd.DataFrame(data)

colours = ['Blue', 'Purple', 'Red', 'Orange']

# Begin plot
sns.boxplot(data=df, orient='h', palette=colours)

plt.xlabel('Volume Expansion [%]', fontsize=16)
plt.savefig('MACE/figures/md_volume.png')
plt.savefig('MACE/figures/md_volume.svg')
plt.show()
'''



chgnet = []
m3gnet = []
mace = []
orb = []
dft = []
exp = []

dir1 = os.listdir('MACE/materials/for_md/chgnet/')
dir2 = os.listdir('MACE/materials/for_md/m3gnet/')
dir3 = os.listdir('MACE/materials/for_md/mace/')
dir4 = os.listdir('MACE/materials/for_md/orb/')
dir6 = os.listdir('MACE/materials/for_md/exp/')

for item in dir1:
    chgnet.append(io.read('MACE/materials/for_md/chgnet/' + item))
for item in dir2:
    m3gnet.append(io.read('MACE/materials/for_md/m3gnet/' + item))
for item in dir3:
    mace.append(io.read('MACE/materials/for_md/mace/' + item))
for item in dir4:
    orb.append(io.read('MACE/materials/for_md/orb/' + item))
for item in dir6:
    exp.append(io.read('MACE/materials/for_md/exp/' + item))
    print(item)


def expansion(file, expt):



    # Get volumes from object
    v1 = file.get_volume()
    v2 = expt.get_volume()

    # print(v1, v2)
    return ((v1/v2) - 1) * 100

c = []
m3 = []
m = []
o = []

for i in range(len(exp)):
    c.append(expansion(chgnet[i], exp[i]))
    m3.append(expansion(m3gnet[i], exp[i]))
    m.append(expansion(mace[i], exp[i]))
    o.append(expansion(orb[i], exp[i]))

data = {
    'CHGNet' : c,
    # 'M3GNet' : m3,
    'MACE' : m,
    'ORB' : o,
}

# Convert to pandas
df = pd.DataFrame(data)

colours = ['Blue', 'Red', 'Orange']

# Begin plot
sns.boxplot(data=df, orient='h', palette=colours)

plt.xlabel('Volume Expansion [%]', fontsize=16)
plt.savefig('MACE/figures/md_volume_no_m3gnet.png')
plt.savefig('MACE/figures/md_volume_no_m3gnet.svg')
plt.show()



'''
# Create a set of subplots in a single column with seven subplots
fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)

# Define different markers and colors for each point
materials = ['LAGP', 'LGPS', 'LSnPS']

# Loop through each subplot and create a number line
for i, ax in enumerate(axes):

    # Plot different markers
    ax.scatter(c[i], 0, label='chgnet', color='Blue', marker='o', s=60)
    ax.scatter(m3[i], 0, label='m3gnet', color='Purple', marker='v', s=60)
    ax.scatter(m[i], 0, label='mace', color='Red', marker='s', s=60)
    ax.scatter(o[i], 0, label='orb', color='Orange', marker='D', s=60)

    # Customize the appearance
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_ylabel(materials[i], fontsize=16)
    ax.grid(False)  # Remove gridlines

    # Remove borders (spines) around each subplot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

# Adjust layout to further decrease space between subplots
plt.tight_layout(rect=[0, 0, 0, 0])
plt.xlabel('Volume Expansion [%]', fontsize=16)
plt.subplots_adjust(hspace=0)

# Show the plot
plt.savefig('MACE/figures/md_volume_2.png')
plt.savefig('MACE/figures/md_volume_2.svg')
plt.show()
'''

'''
# Create a set of subplots in a single column with seven subplots
fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)

# Define different markers and colors for each point
materials = ['LAGP', 'LGPS', 'LSnPS']

# Loop through each subplot and create a number line
for i, ax in enumerate(axes):

    # Plot different markers
    ax.scatter(c[i], 0, label='chgnet', color='Blue', marker='o', s=60)
    # ax.scatter(m3[i], 0, label='m3gnet', color='Purple', marker='v', s=60)
    ax.scatter(m[i], 0, label='mace', color='Red', marker='s', s=60)
    ax.scatter(o[i], 0, label='orb', color='Orange', marker='D', s=60)

    # Customize the appearance
    ax.set_yticks([])  # Remove y-axis ticks
    ax.set_ylabel(materials[i], fontsize=16)
    ax.grid(False)  # Remove gridlines

    # Remove borders (spines) around each subplot
    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['bottom'].set_visible(False)

# Adjust layout to further decrease space between subplots
plt.tight_layout(rect=[0, 0, 0, 0])
plt.xlabel('Volume Expansion [%]', fontsize=16)
plt.subplots_adjust(hspace=0)

# Show the plot
plt.savefig('MACE/figures/md_volume_2_no_m3g.png')
plt.savefig('MACE/figures/md_volume_2_no_m3g.svg')
plt.show()
'''