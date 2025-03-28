#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=00:30:00
#SBATCH --cpus-per-task=16

# module load gcc
# module load gnuplot
# module load hisat2
# module load sra-toolkit
# module load trimmomatic
# module load fastqc
module load fastp
bash qc.sh -r SRR15049591,SRR15049592,SRR15049593 -d ../../operons/data_odb/txid224308 -l P
bash qc.sh -r SRR7977557,SRR7977561,SRR7977565 -d ../../operons/data_odb/txid196627 -l P
bash qc.sh -r SRR1787590,SRR1787592,SRR1787594 -d ../../operons/data_odb/txid511145 -l P
bash qc.sh -r SRR5217495,SRR5217496 -d ../../operons/data_odb/txid85962 -l P
bash qc.sh -r ERR1157043,ERR1157044,ERR1157045 -d ../../operons/data_odb/txid297246 -l S
bash qc.sh -r SRR11998214,SRR11998215,SRR11998216 -d ../../operons/data_odb/txid169963 -l S
bash qc.sh -r ERR3672190,ERR3672191,ERR3672191 -d ../../operons/data_odb/txid272634 -l P
# bash qc.sh -r ?,?, -d ../../operons/data_odb/txid298386 -l ?
bash qc.sh -r SRR14432343,SRR14432344,SRR14432345 -d ../../operons/data_odb/txid176299 -l S
bash qc.sh -r SRR11997800,SRR11997801,SRR11997802 -d ../../operons/data_odb/txid224326 -l S
bash qc.sh -r SRR8955127,SRR8955139 -d ../../operons/data_odb/txid224911 -l P
bash qc.sh -r SRR11998427,SRR11998428,SRR11998429 -d ../../operons/data_odb/txid208964 -l P
bash qc.sh -r SRR5489122,SRR5489125 -d ../../operons/data_odb/txid214092 -l S