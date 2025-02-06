#!/bin/bash
#SBATCH --ntasks=1
#SBATCH --gres=gpu:v100:1
#SBATCH --cpus-per-task=3
#SBATCH --mem-per-cpu=4G
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=Li_batt_all
#SBATCH --account=def-ravh011
#SBATCH --time=4:00:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

python "$HOME/projects/rrg-ravh011/cgurwell/Ion_Channels/Code/bvel_all.py" "Li1+" 10.0 0.05 100 5.0