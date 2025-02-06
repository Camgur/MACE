from pymatgen.core import Structure
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer
from pymatgen.transformations.advanced_transformations import EnumerateStructureTransformation
from pymatgen.io.vasp.sets import batch_write_input, MPRelaxSet

# Choose file
filename = 'MACE\optimise\disordered\LAGP_263763.cif'
# filename = 'LGPS_30161.cif'

# Import Disordered CIF
structure = structure = Structure.from_file(filename)
# print(structure)



# loop over all sites in the structure
for i, site in enumerate(structure):

    # Fix the occupancy
    if not site.is_ordered:
        # print(structure[i].species_string)

        if structure[i].species_string == "Al3+:0.24, Ge4+:0.76":
            structure[i] = {"Al3+": 0.25, "Ge4+": 0.75}

        if structure[i].species_string == "Li+:0.65":
            structure[i] = {"Li+": 0.66}

        if structure[i].species_string == "Li+:0.139":
            structure[i] = {"Li+": 0.14}


print("The composition after adjustments is %s." % structure.composition.reduced_formula)


# Find Primitive Spacegroup
analyzer = SpacegroupAnalyzer(structure)
prim_cell = analyzer.find_primitive()
print(prim_cell)



# Create symmetry-based output based on disordered CIF
enum = EnumerateStructureTransformation(min_cell_size=2, max_cell_size=20)
structures = enum.apply_transformation(structure, return_ranked_list=100)

print(len(structures))
print("cell sizes are %s" % ([len(d["structure"]) for d in structures]))

# assert 0

# Write to CIF
# The following two lines write all the structures to CIF files with names CuAu_0.cif, CuAu_1.cif, ...
for i, d in enumerate(structures):
    d["structure"].to(filename=filename.replace('.cif', '/') + filename.replace('.cif', '') + "_%d.cif" % i)