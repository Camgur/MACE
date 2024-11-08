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
python Li3Fe2PO43_neb_delithiated.py Li3Fe2PO43_98361_delithiated.cif 78 74 Li3Fe2PO43_98361.cif

python Li3Fe2PO43_neb_delithiated.py Li3Fe2PO43_98361_delithiated.cif 78 70 Li3Fe2PO43_98361.cif

python Li3Fe2PO43_neb_delithiated.py Li3Fe2PO43_98361_delithiated.cif 71 75 Li3Fe2PO43_98361.cif
