#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=5:00:00
#SBATCH --mem-per-cpu=13G


module load gcc
module load sra-toolkit

# mkdir ../data_odb
bash sra.sh -r SRR15049591,SRR15049592,SRR15049593 -t 224308 -o ../data_odb
# bash sra.sh -r SRR7977557,SRR7977561,SRR7977565 -t 196627 -o ../data_odb
# bash sra.sh -r SRR1787590,SRR1787592,SRR1787594 -t 511145 -o ../data_odb
bash sra.sh -r SRR7217927,SRR7217928,SRR7217929,SRR7217930 -t 511145 -o ../data_odb
# bash sra.sh -r SRR5217495,SRR5217496, -t 85962 -o ../data_odb
# bash sra.sh -r ERR1157043,ERR1157044,ERR1157045 -t 297246 -o ../data_odb
# bash sra.sh -r SRR11998214,SRR11998215,SRR11998216 -t 169963 -o ../data_odb
bash sra.sh -r SRR11998208,SRR11998211,SRR11998217,SRR11998220,SRR11998223 -t 169963 -o ../data_odb
bash sra.sh -r ERR3672190,ERR3672191,ERR3672191 -t 272634 -o ../data_odb
# bash sra.sh -r SRR500950,SRR500951 -t 298386 -o ../data_odb
# bash sra.sh -r SRR14432343,SRR14432344,SRR14432345 -t 176299 -o ../data_odb
# bash sra.sh -r SRR11997800,SRR11997801,SRR11997802 -t 224326 -o ../data_odb
# bash sra.sh -r SRR13238987,SRR13238988,SRR13238989 -t 224911 -o ../data_odb
# bash sra.sh -r SRR11998427,SRR11998428,SRR11998429 -t 208964 -o ../data_odb
# bash sra.sh -r SRR5489122,SRR5489125 -t 214092 -o ../data_odb
# bash sra.sh -r SRR11605370,SRR11605378,SRR11605385 -t 6239 -o ../data_odb