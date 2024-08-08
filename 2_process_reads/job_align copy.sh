#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=00:30:00
#SBATCH --mem-per-cpu=8G
#SBATCH --cpus-per-task=16

module load hisat2
module load samtools
module load bedtools

# 14866306

# without qc
# bash align.sh -r SRR11998214,SRR11998215,SRR11998216 -d ../../operons/data_odb/txid169963 -l S -q N -f txid169963.fasta
# bash align.sh -r SRR11997800,SRR11997801,SRR11997802 -d ../../operons/data_odb/txid224326 -l S -q N -f txid224326.fasta
# bash align.sh -r SRR11998427,SRR11998428,SRR11998429 -d ../../operons/data_odb/txid208964 -l P -q N -f txid208964.fasta

# with qc
# bash align.sh -r SRR15049591,SRR15049592,SRR15049593 -d ../../operons/data_odb/txid224308 -l P -q Y -f txid224308.fasta
# bash align.sh -r SRR7977557,SRR7977561,SRR7977565 -d ../../operons/data_odb/txid196627 -l P -q Y -f txid196627.fasta
# bash align.sh -r SRR1787590,SRR1787592,SRR1787594 -d ../../operons/data_odb/txid511145 -l P -q Y -f txid511145.fasta
bash align.sh -r SRR5217495,SRR5217496 -d ../../operons/data_odb/txid85962 -l P -q Y -f txid85962.fasta
# bash align.sh -r ERR1157043,ERR1157044,ERR1157045 -d ../../operons/data_odb/txid297246 -l S -q Y -f txid297246.fasta
# bash align.sh -r ERR3672190,ERR3672191,ERR3672191 -d ../../operons/data_odb/txid272634 -l P -q Y -f txid272634.fasta
# bash align.sh -r ?,?, -d ../../operons/data_odb/txid298386 -l ? -q Y -f txid298386.fasta
# bash align.sh -r SRR14432343,SRR14432344,SRR14432345 -d ../../operons/data_odb/txid176299 -l S -q Y -f txid176299.fasta
# bash align.sh -r SRR8955127,SRR8955139 -d ../../operons/data_odb/txid224911 -l P -q Y -f txid224911.fasta
# bash align.sh -r SRR5489122,SRR5489125 -d ../../operons/data_odb/txid214092 -l S -q Y -f txid214092.fasta