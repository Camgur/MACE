import sys
import os
import numpy as np
import pandas as pd
import logging

from ase.io import read
from ase import atoms

from bvlain import Lain

x=0

# Create Filenames List
filenames = []

# Create Energies Lists
E_1D, E_2D, E_3D = [], [], []

# Set Folder
folder = sys.argv[1]
# folder = r'C:\Users\camgu\Goward Group\Code\Ion_Channels\Code\cif'

# Iterate in Folder
for filename in os.listdir(folder):

	# Set File
	file = os.path.join(folder, filename)
	base = r'C:\Users\camgu\Goward Group\Code\Ion_Channels'

	# Filter CIFs
	if file.endswith('.cif'):
		atoms = read(file)

		try:
			# Check has Li (Some are cathode materials)
			if 'Li' not in atoms.get_chemical_symbols():
				continue
			
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

			# Append Filenames List
			filenames.append(filename.replace('.cif', ''))

			# Separate Energies
			E_1D.append(energies['E_1D'])
			E_2D.append(energies['E_2D'])
			E_3D.append(energies['E_3D'])
			x+=1
			if x >= 3:
				break
		except:
			print(filename, '\n', atoms.get_chemical_formula(), '\n')
			pass

# Create Headers
header = ['mpID', 'E_1D', 'E_2D', 'E_3D']

# Compilation of Values
data = np.array([filenames, E_1D, E_2D, E_3D])
data = data.T

# Write to CSV
data = pd.DataFrame(data, columns=header)
# print(data)
data.to_csv(base + r'\bvse.csv', encoding='utf-8', index=False)