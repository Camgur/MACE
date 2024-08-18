import sys
import os
import numpy as np
import pandas as pd
import csv

from bvlain import Lain

# Set File
file = sys.argv[1]
filename = os.path.basename(file)
base = r'C:\Users\camgu\Goward Group\Code\Ion_Channels'

# Set Lain Calculator
calc = Lain(verbose = True)
calc.read_file(file)

# Set BVSE Params (Determined in CMD)
params = {'mobile_ion': sys.argv[2],
		  'r_cut': float(sys.argv[3]),
		  'resolution': float(sys.argv[4]),
		  'k': float(sys.argv[5])
}

# Calculate BVSE
calc.bvse_distribution(**params)
energies = calc.percolation_barriers(encut = float(sys.argv[6]))

# Write Grid File
calc.write_grd(base + '\\' + filename.replace('.cif', ''))

# Create Headers
header = ['mpID', 'E_1D', 'E_2D', 'E_3D']

# Create Filenames List
filenames = []
filenames.append(filename.replace('.cif', ''))

# Separate Energies
E_1D, E_2D, E_3D = [], [], []
E_1D.append(energies['E_1D'])
E_2D.append(energies['E_2D'])
E_3D.append(energies['E_3D'])

# Compilation of Values
data = [filenames, E_1D, E_2D, E_3D]

# Write to CSV
data = pd.DataFrame([data], columns=header)
# print(data)
data.to_csv(base + r'\bvse.csv', encoding='utf-8', index=False)