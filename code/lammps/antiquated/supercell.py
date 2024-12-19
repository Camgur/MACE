from ase.io.lammpsdata import write_lammps_data, read_lammps_data
from ase.io import read
from ase.build.supercells import make_supercell
from ase.visualize import view

# Make Supercell 4x4
matrix = [[4, 0, 0], [0, 4, 0], [0, 0, 4]]

cif = read('MACE\lattice\LiAlO2_430184_opt.cif')
make = make_supercell(cif, matrix)

write_lammps_data('MACE\materials\LiAlO2_430184.lmpdat',
                  make, masses=True, units='metal', bonds=False, atom_style='atomic')

supercell = read_lammps_data('MACE\materials\LiAlO2_430184.lmpdat')
view(supercell)