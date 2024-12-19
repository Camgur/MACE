#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=4
#SBATCH --mem=64G
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=QE_relax_LZPO
#SBATCH --account=def-ravh011
#SBATCH --time=4-00:00:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

module load StdEnv/2023  gcc/12.3  openmpi/4.1.5
module load quantumespresso/7.3.1

# SCF Calc
mpirun pw.x -in LZPO_relax.in > LZPO_relax.out
