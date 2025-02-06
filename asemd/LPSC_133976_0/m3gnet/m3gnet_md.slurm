#!/bin/bash
#SBATCH --nodes=1
#SBATCH --tasks-per-node=1
#SBATCH --error=error.txt
#SBATCH --output=output.txt
#SBATCH --job-name=md_m3gnet_LPSC
#SBATCH --account=def-ravh011
#SBATCH --time=20:00
#SBATCH --mail-user=gurwellc@mcmaster.ca
#SBATCH --mail-type=ALL

# Loop temperatures
temp="298.15 308.15 318.15 328.15 338.15 348.15 358.15"
for i in $temp; do

    # Concatenate input script with list temp
    # Run repeat otherwise setup for MD ends the run prematurely
    a='module purge
module load cuda cudann
module load python/3.10
source ~/chgnet/bin/activate
python m3gnet_md.py ../LPSC_133976_0.cif'
    b='
while (( SECONDS <= 100 )); do
    echo "Running"
    sleep 10 || break
done
echo "Done"'
    foo="${a} ${i} ${b}"

    # Submit job to cluster
    sbatch --nodes=1 --tasks-per-node=3 --mem=12G --gpus-per-node=v100l:1 --time=10:00:00 --job-name=${i}_m3gnet_LPSC --wrap="$foo"
done