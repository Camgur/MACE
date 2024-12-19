#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=3
#SBATCH --gres=gpu:p100:1
#SBATCH --mem=12G
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=opt_mace_LiFeV2O7_lith
#SBATCH --account=def-ravh011
#SBATCH --time=0:20:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL


# Load environment
module purge
module load python/3.11 StdEnv/2023
source ~/MACE/bin/activate


# Run scripts
python opt_mace.py ../LiFeV2O7_lith.cif
