import os
# Disable JIT 
# os.environ['PYTORCH_JIT'] = '0'

from mpi4py import MPI
from lammps.pylammps import PyLammps

lmp = PyLammps()
lmp.file("LiAlO2.in")
me = MPI.COMM_WORLD.Get_rank()
nprocs = MPI.COMM_WORLD.Get_size()
print("Proc %d out of %d procs has" % (me,nprocs),lmp)
MPI.Finalize()