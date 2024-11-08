#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=8
#SBATCH --mem=64G
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=lammps_mace
#SBATCH --account=def-ravh011
#SBATCH --time=0:10:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL


# Set OMP Threads variable
$OMP_NUM_THREADS=16


# Load environment
module purge
module load python/3.10.13 StdEnv/2023
source ~/MACE/bin/activate


# Run scripts
mpirun -np 8 python lamp.py