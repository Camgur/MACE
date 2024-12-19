#!/bin/sh
# This script was created by sbatch --wrap.

module purge, module load python/3.10, source ~/chgnet/bin/activate, python chgnet_md.py ../LiAlO2_430184.cif $i
