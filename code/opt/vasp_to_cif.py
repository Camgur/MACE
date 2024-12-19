from ase.io import read, write
from ase.visualize import view
from ase.spacegroup import get_spacegroup, symmetrize

file = read('MACE\optimise\Li3Fe2PO43_98361\CONTCAR', format='vasp')

view(file)

write('MACE\optimise\Li3Fe2PO43_98361\LFVO_opt.cif', file)