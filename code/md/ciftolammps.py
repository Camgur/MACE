from ase import build, units, atoms
from ase.io import read, write, Trajectory
from ase.io.lammpsdata import write_lammps_data

atoms = read(r"C:\Users\camgu\Goward Group\Code\ion_channels_data\lammps_dat\mp-1178027.cif")

write_lammps_data(file=r"C:\Users\camgu\Goward Group\Code\ion_channels_data\lammps_dat\mp-1178027.lmp",
                  atoms=atoms)