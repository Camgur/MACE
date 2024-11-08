#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gpus-per-node=p100:1
#SBATCH --tasks-per-node=8
#SBATCH --mem=16G
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=neb_chgnet
#SBATCH --account=def-ravh011
#SBATCH --time=4:00:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

module purge
module load python/3.11.5 scipy-stack rust

# Activate virtual environment
source ~/MACE/bin/activate

# Run scripts
python neb_chgnet.py LiFeV2O7-Article.cif 129 120