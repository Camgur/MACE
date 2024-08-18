#!/bin/bash
#SBATCH --nodes=1 # number of nodes
#SBATCH --ntasks-per-node=40
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=Li_battery_descent
#SBATCH --account=def-ravh011
#SBATCH --time=00:05:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

python "$HOME/projects/rrg-ravh011/cgurwell/Ion_Channels/Code/opt.py" "$HOME/projects/rrg-ravh011/cgurwell/Ion_Channels/Code/cif/mp-752786.cif"
