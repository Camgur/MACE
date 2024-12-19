#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=4
#SBATCH --mem=64G
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=QE_nmr_LZPO
#SBATCH --account=def-ravh011
#SBATCH --dependency=afterok:26862267
#SBATCH --time=02:00:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

module load StdEnv/2023  gcc/12.3  openmpi/4.1.5
module load quantumespresso/7.3.1

# NMR Calc
mpirun gipaw.x -in LZPO_nmr.in > LZPO_nmr.out

# EFG Calc
#mpirun gipaw.x -in LZPO_efg.in > LZPO_efg.out
