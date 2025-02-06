#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --gpus-per-task=v100:4
#SBATCH --mem-per-gpu=16G
#SBATCH --cpus-per-task=12
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=Li_lammps_gpu
#SBATCH --account=def-ravh011
#SBATCH --time=1:00:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

module purge
module load StdEnv/2023 intel/2023.2.1 cuda openmpi/4.1.5 lammps-omp/20230802

lmp -k on g 1 -sf kk -in mp-1178027.in