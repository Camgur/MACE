#!/bin/bash
#SBATCH --nodes=1
#SBATCH --gpus_per_node=p100:1
#SBATCH --tasks-per-node=8
#SBATCH --mem=16G
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=neb_Li3Fe2PO43
#SBATCH --account=def-ravh011
#SBATCH --time=8:00:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

module purge
module load python/3.11.5 scipy-stack rust

# Activate virtual environment
source ~/MACE/bin/activate

# Run scripts
python Li3Fe2Po43_ml_neb.py Li3Fe2PO43_98361.cif 78 74

python Li3Fe2Po43_ml_neb.py Li3Fe2PO43_98361.cif 78 70

python Li3Fe2Po43_ml_neb.py Li3Fe2PO43_98361.cif 71 75