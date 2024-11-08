#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gpus-per-node=p100:1
#SBATCH --tasks-per-node=8
#SBATCH --mem=16G
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=alt_neb_Li3Fe2PO43
#SBATCH --account=def-ravh011
#SBATCH --time=2:00:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

module purge
module load python/3.11.5 scipy-stack rust

# Activate virtual environment
source ~/MACE/bin/activate

# Run scripts
python LFVO_neb_delithiated.py LiFeV2O7_delithiated.cif 129 120 LiFeV2O7-Article.cif

python LFVO_neb_delithiated.py LiFeV2O7_delithiated.cif 120 125 LiFeV2O7-Article.cif

python LFVO_neb_delithiated.py LiFeV2O7_delithiated.cif 129 125 LiFeV2O7-Article.cif
