#!/bin/sh
# This script was created by sbatch --wrap.

module purge\n
    echo ${i}\n
    module load python/3.10\n
    echo ${i}\n
    source ~/chgnet/bin/activate\n
    echo ${i}\n
    python chgnet_md.py ../LiAlO2_430184.cif ${i}\n
    echo ${i}
