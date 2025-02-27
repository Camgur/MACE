import os
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
from ase import io

# Function to load structures from directories
def load_structures(base_path, categories):
    structures = {category: [] for category in categories}
    for category in categories:
        path = os.path.join(base_path, category)
        for file in os.listdir(path):
            structures[category].append(io.read(os.path.join(path, file)))
    return structures

# Function to compute volume expansion
def volume_expansion(model, exp_ref):
    return ((model.get_volume() / exp_ref.get_volume()) - 1) * 100

# Define categories for comparison
categories = ['chgnet', 'm3gnet', 'mace', 'orb', 'dft', 'exp']

# Load structures
materials_path = 'MACE/materials/for_compare'
structures = load_structures(materials_path, categories)

# Compute volume expansions
exp = structures['exp']
volume_data = {cat: [volume_expansion(structures[cat][i], exp[i]) for i in range(len(exp))] 
               for cat in categories if cat != 'exp'}

# Convert to DataFrame
def plot_boxplot(volume_data, exclude_m3gnet=False, subset=None, exclude_dft=False, filename_suffix=""):
    df = pd.DataFrame(volume_data)
    if exclude_m3gnet:
        df = df.drop(columns=['m3gnet'])
    if exclude_dft:
        df = df.drop(columns=['dft'])
    if subset:
        df = df.iloc[:len(subset)]
    
    palette = ['Blue', 'Red', 'Orange'] if exclude_m3gnet and exclude_dft else \
              ['Blue', 'Red', 'Orange', 'Turquoise'] if exclude_m3gnet else \
              ['Blue', 'Purple', 'Red', 'Orange', 'Turquoise']
    sns.boxplot(data=df, orient='h', palette=palette)
    plt.xlabel('Volume Expansion [%]', fontsize=16)
    plt.legend(title='Model', labels=df.columns, loc='upper right')
    plt.savefig(f'MACE/figures/md_volume{filename_suffix}.png')
    plt.savefig(f'MACE/figures/md_volume{filename_suffix}.svg')
    plt.show()

# Generate both box plots
plot_boxplot(volume_data, exclude_m3gnet=False)
plot_boxplot(volume_data, exclude_m3gnet=True)

# Generate box plot for LAGP, LGPS, and LSnPS dataset without DFT results
materials_subset = ['LAGP', 'LGPS', 'LSnPS']

# Load structures
materials_path = 'MACE/materials/for_compare'
structures = load_structures(materials_path, categories)

plot_boxplot(volume_data, exclude_m3gnet=False, subset=materials_subset, exclude_dft=True, filename_suffix="_for_md")
plot_boxplot(volume_data, exclude_m3gnet=True, subset=materials_subset, exclude_dft=True, filename_suffix="_for_md_no_m3gnet")

# Create subplots for individual material comparisons
def plot_comparisons(volume_data, exclude_m3gnet=False, exclude_dft=False):
    materials = ['LAGP', 'LGPS', 'LSnPS']
    fig, axes = plt.subplots(nrows=3, ncols=1, sharex=True)

    for i, ax in enumerate(axes):
        ax.axhline(y=0, color='Black', linestyle='--', zorder=0)  # Add horizontal line behind data
        
        ax.scatter(volume_data['chgnet'][i], 0, label='chgnet', color='Blue', marker='o', s=60, zorder=1)
        if not exclude_m3gnet:
            ax.scatter(volume_data['m3gnet'][i], 0, label='m3gnet', color='Purple', marker='v', s=60, zorder=1)
        ax.scatter(volume_data['mace'][i], 0, label='mace', color='Red', marker='s', s=60, zorder=1)
        ax.scatter(volume_data['orb'][i], 0, label='orb', color='Orange', marker='D', s=60, zorder=1)
        if not exclude_dft:
            ax.scatter(volume_data['dft'][i], 0, label='dft', color='Turquoise', marker='h', s=60, zorder=1)
        
        ax.set_yticks([])
        ax.set_ylabel(materials[i], fontsize=16, rotation=0, labelpad=40)
        ax.grid(False)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_visible(False)
        ax.spines['bottom'].set_visible(False)
    
    handles, labels = ax.get_legend_handles_labels()
    fig.legend(handles, labels, title='Model', loc='upper right', fontsize=12)
    
    plt.tight_layout(rect=[0, 0, 0, 0])
    plt.xlabel('Volume Expansion [%]', fontsize=16)
    plt.subplots_adjust(hspace=0)
    suffix = '_no_m3gnet' if exclude_m3gnet else ''
    suffix += '_no_dft' if exclude_dft else ''
    plt.savefig(f'MACE/figures/md_volume_comparison{suffix}.png')
    plt.savefig(f'MACE/figures/md_volume_comparison{suffix}.svg')
    plt.show()

# Generate both scatter plots excluding DFT results for LAGP, LGPS, LSnPS
plot_comparisons(volume_data, exclude_m3gnet=False, exclude_dft=True)
plot_comparisons(volume_data, exclude_m3gnet=True, exclude_dft=True)