import os
import json
from pymatgen.io.cif import CifParser

import warnings
warnings.simplefilter("ignore")

# Importing function for directory
def load_structures(base_path):
    structures = []
    ids = []
    for file in os.listdir(base_path):
        ids.append(file)
        parser = CifParser(filename=os.path.join(base_path, file))
        structures.append(parser.parse_structures()[0])
    return ids, structures

# Return ids and structures from function
ids, structures = load_structures('MACE/materials/for_opt')

# Convert structures to a dictionary format
structures_dict = [structure.as_dict() for structure in structures]

# Form dictionary
objects = {
    'id' : ids,
    'structure' : structures_dict
}

# Store dict as json data, with structures as a dict object
with open('MACE/materials/materials_data.json', 'w') as f:
    json.dump(objects, f, indent=4)


# print(obj.composition.get_reduced_formula_and_factor()[0])