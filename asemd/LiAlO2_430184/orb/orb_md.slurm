#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=md_orb_LiAlO2
#SBATCH --account=def-ravh011
#SBATCH --time=20:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

# Loop over temperature
temp='298.15 308.15 318.15 328.15 338.15 348.15 358.15'
for i in $temp; do

    # Concatenate input script with list temp
    # Run repeat otherwise setup for MD ends the run prematurely
    a='module purge
module load python/3.10
source ~/orb/bin/activate
python orb_md.py ../LiAlO2_430184.cif'
    b='
while (( SECONDS <= 100 )); do
    echo "Running"
    sleep 10 || break
done
echo "Done"'
    foo="${a} ${i} ${b}"

    # Submit job to cluster
    sbatch --nodes=1 --tasks-per-node=3 --mem=12G --gpus-per-node=v100l:1 --time=04:00:00 --job-name=${i}_orb_LiAlO2 --wrap="$foo"
done