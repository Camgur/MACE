from pymatgen.transformations.advanced_transformations import EnumerateStructureTransformation, OrderDisorderedStructureTransformation
from pymatgen.io.cif import CifParser

# Choose file
filename = 'LAGP_263763.cif'
# filename = 'LGPS_30161.cif'

# Import Disordered CIF
file = CifParser(filename)
structure = file.parse_structures(primitive=True)[0]

# Create symmetry-based output based on disordered CIF
# transform = EnumerateStructureTransformation(min_cell_size=2, max_cell_size=4)
transform = OrderDisorderedStructureTransformation()
out = transform.apply_transformation(structure, return_ranked_list=1000)


print(len(out))
print("cell sizes are %s" % ([len(d["structure"]) for d in out]))

# Write to CIF
# The following two lines write all the structures to CIF files with names CuAu_0.cif, CuAu_1.cif, ...
for i, d in enumerate(out):
    d["structure"].to(filename=filename.replace('.cif', '/') + filename.replace('.cif', '') + "_%d.cif" % i)