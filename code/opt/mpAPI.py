import os
import time
from mp_api.client import MPRester

# Find relative directory
module_path = os.path.dirname(os.path.realpath(__file__))

# Initialise MPRester class
mpr = MPRester(api_key='n2wdTtixZm1iaLdGBjboJmEEv4TEc4zl')

# Get structures
structures = mpr.materials.insertion_electrodes.search(working_ion='Li', fields='material_ids')

# Parse structures
for i, structure in enumerate(structures):

    # Convert the structure to a CIF string and save to a CIF file
    id = structure.material_ids
    cif = mpr.get_structure_by_material_id(id)
    print(i, type(cif))

    # Skip bad data
    if cif.__class__ != 'pymatgen.core.structure.Structure':
        continue

    cif_data = cif.to(fmt="cif")

    # Set output directory
    output = os.path.join(module_path, 'cif', id[0] + '.cif')

    # Write to CIF
    with open(output, "w") as f:
        f.write(cif_data)

    # Counter for server spamming
    if i%100 == 0:
        time.sleep(5)