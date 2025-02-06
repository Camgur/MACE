from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.transformations.advanced_transformations import EnumerateStructureTransformation, OrderDisorderedStructureTransformation
from pymatgen.io.vasp.sets import batch_write_input, MPRelaxSet

# Choose file
filename = r'MACE\optimise\disordered\tutorial\LPSC_418490.cif'
# filename = 'LGPS_30161.cif'

# Import Disordered CIF
structure = Structure.from_file(filename)
# print(structure)



# loop over all sites in the structure
for i, site in enumerate(structure):
    # change the occupancy of Li+ disordered sites to 0.5
    if not site.is_ordered:
        structure[i] = {"Li+": 0.5}
print("The composition after adjustments is %s." % structure.composition.reduced_formula)


# Find Primitive Spacegroup
analyzer = SpacegroupAnalyzer(structure)
prim_cell = analyzer.find_primitive()
print(prim_cell)



# Create symmetry-based output based on disordered CIF

# Don't use enum if possible, it's kinda shit
# enum = EnumerateStructureTransformation(check_ordered_symmetry=False, max_cell_size=1)

order = OrderDisorderedStructureTransformation(algo=0, symmetrized_structures=False, no_oxi_states=False)
structures = order.apply_transformation(structure, return_ranked_list=20)

print(len(structures))
print("cell sizes are %s" % ([len(d["structure"]) for d in structures]))

# assert 0

# Write to CIF
# The following two lines write all the structures to CIF files with names CuAu_0.cif, CuAu_1.cif, ...
for i, d in enumerate(structures):
    d["structure"].to(filename=filename.replace('.cif', '/') + filename.replace('.cif', '') + "_%d.cif" % i)