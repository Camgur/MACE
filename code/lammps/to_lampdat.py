from ase.io.lammpsdata import write_lammps_data

write_lammps_data(fd, atoms: Atoms, *, specorder: list = None, reduce_cell: bool = False, force_skew: bool = False, prismobj: Prism = None, write_image_flags: bool = False, masses: bool = False, velocities: bool = False, units: str = 'metal', bonds: bool = True, atom_style: str = 'atomic')