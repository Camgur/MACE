#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --job-name=md_m3gnet_LSnPS
#SBATCH --account=def-ravh011
#SBATCH --time=10:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL


# Loop over temperature
temp='300.0 400.0 500.0 600.0'
for i in $temp; do

    # Concatenate input script with list temp
    # Run repeat otherwise setup for MD ends the run prematurely
    a='module purge
module load cuda cudann
module load python/3.10
source ~/env/m3gnet/bin/activate
python m3gnet_md.py opt_LSnPS.cif'
    b='
while (( SECONDS <= 21000 )); do
    echo "Running"
    sleep 1000 || break
done
echo "Done"'
    foo="${a} ${i} ${b}"

    # Submit job to cluster
    sbatch --nodes=1 --tasks-per-node=1 --mem=12G --gpus-per-node=v100l:1 --time=12:00:00 --job-name=${i}_m3gnet_LSnPS --wrap="$foo"
done