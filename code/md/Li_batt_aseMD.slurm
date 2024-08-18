#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --gpus-per-task=v100:1
#SBATCH --mem-per-gpu=16G
#SBATCH --cpus-per-task=3
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=Li_batt_aseMD
#SBATCH --account=def-ravh011
#SBATCH --time=10:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

python "$HOME/projects/rrg-ravh011/cgurwell/Ion_Channels/Code/aseMD.py" "$HOME/scratch/optimise/mp-1178027.cif"