#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=02:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4

# virtualenv --no-download operonSEQer_env
module load java

# pip install -r 6_os_req.txt

DIR='../../operons/data_odb/'

# ------------------ Train ------------------
# mkdir ${DIR}txid224308/txid224308/
# cp ${DIR}txid224308/txid224308.fasta ${DIR}txid224308/txid224308/txid224308.fna
# python 4_convert_gff3.py ${DIR}txid224308/txid224308.gff3 ${DIR}txid224308/txid224308/txid224308
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid224308/SRR15049591_1.fastq%${DIR}txid224308/SRR15049591_2.fastq,${DIR}txid224308/SRR15049592_1.fastq%${DIR}txid224308/SRR15049592_2.fastq,${DIR}txid224308/SRR15049593_1.fastq%${DIR}txid224308/SRR15049593_2.fastq,${DIR}txid224308/ERR6156944_1.fastq%${DIR}txid224308/ERR6156944_2.fastq,${DIR}txid224308/ERR6156945_1.fastq%${DIR}txid224308/ERR6156945_2.fastq,${DIR}txid224308/ERR6156946_1.fastq%${DIR}txid224308/ERR6156946_2.fastq -o ${DIR}txid224308/rh_outputs/txid224308 -g ${DIR}txid224308/txid224308

# mkdir ${DIR}txid196627/txid196627/
# cp ${DIR}txid196627/txid196627.fasta ${DIR}txid196627/txid196627/txid196627.fna
# python 4_convert_gff3.py ${DIR}txid196627/txid196627.gff3 ${DIR}txid196627/txid196627/txid196627
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid196627/SRR7977557_1.fastq%${DIR}txid196627/SRR7977557_2.fastq,${DIR}txid196627/SRR7977561_1.fastq%${DIR}txid196627/SRR7977561_2.fastq,${DIR}txid196627/SRR7977565_1.fastq%${DIR}txid196627/SRR7977565_2.fastq,${DIR}txid196627/ERR3380462_1.fastq%${DIR}txid196627/ERR3380462_2.fastq,${DIR}txid196627/ERR3380465_1.fastq%${DIR}txid196627/ERR3380465_2.fastq,${DIR}txid196627/ERR3380468_1.fastq%${DIR}txid196627/ERR3380468_2.fastq -o ${DIR}txid196627/rh_outputs/txid196627 -g ${DIR}txid196627/txid196627

# mkdir ${DIR}txid511145/txid511145/
# cp ${DIR}txid511145/txid511145.fasta ${DIR}txid511145/txid511145/txid511145.fna
# python 4_convert_gff3.py ${DIR}txid511145/txid511145.gff3 ${DIR}txid511145/txid511145/txid511145
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid511145/SRR1787590_1.fastq%${DIR}txid511145/SRR1787590_2.fastq,${DIR}txid511145/SRR1787592_1.fastq%${DIR}txid511145/SRR1787592_2.fastq,${DIR}txid511145/SRR1787594_1.fastq%${DIR}txid511145/SRR1787594_2.fastq,${DIR}txid511145/SRR7217927_1.fastq%${DIR}txid511145/SRR7217927_2.fastq,${DIR}txid511145/SRR7217928_1.fastq%${DIR}txid511145/SRR7217928_2.fastq,${DIR}txid511145/SRR7217929_1.fastq%${DIR}txid511145/SRR7217929_2.fastq -o ${DIR}txid511145/rh_outputs/txid511145 -g ${DIR}txid511145/txid511145

# mkdir ${DIR}txid85962/txid85962/
# cp ${DIR}txid85962/txid85962.fasta ${DIR}txid85962/txid85962/txid85962.fna
# python 4_convert_gff3.py ${DIR}txid85962/txid85962.gff3 ${DIR}txid85962/txid85962/txid85962
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid85962/SRR5217496_1.fastq%${DIR}txid85962/SRR5217496_2.fastq -o ${DIR}txid85962/rh_outputs/txid85962 -g ${DIR}txid85962/txid85962

# mkdir ${DIR}txid297246/txid297246/
# cp ${DIR}txid297246/txid297246.fasta ${DIR}txid297246/txid297246/txid297246.fna
# python 4_convert_gff3.py ${DIR}txid297246/txid297246.gff3 ${DIR}txid297246/txid297246/txid297246
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid297246/ERR1157043.fastq,${DIR}txid297246/ERR1157044.fastq,${DIR}txid297246/ERR1157045.fastq -o ${DIR}txid297246/rh_outputs/txid297246 -g ${DIR}txid297246/txid297246

# mkdir ${DIR}txid169963/txid169963/
# cp ${DIR}txid169963/txid169963.fasta ${DIR}txid169963/txid169963/txid169963.fna
# python 4_convert_gff3.py ${DIR}txid169963/txid169963.gff3 ${DIR}txid169963/txid169963/txid169963
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid169963/SRR11998208.fastq,${DIR}txid169963/SRR11998211.fastq,${DIR}txid169963/SRR11998214.fastq,${DIR}txid169963/SRR11998217.fastq,${DIR}txid169963/SRR11998220.fastq,${DIR}txid169963/SRR11998223.fastq -o ${DIR}txid169963/rh_outputs/txid169963 -g ${DIR}txid169963/txid169963

# mkdir ${DIR}txid272634/txid272634/
# cp ${DIR}txid272634/txid272634.fasta ${DIR}txid272634/txid272634/txid272634.fna
# python 4_convert_gff3.py ${DIR}txid272634/txid272634.gff3 ${DIR}txid272634/txid272634/txid272634
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid272634/ERR3672190_1.fastq%${DIR}txid272634/ERR3672190_2.fastq,${DIR}txid272634/ERR3672191_1.fastq%${DIR}txid272634/ERR3672191_2.fastq,${DIR}txid272634/ERR3672192_1.fastq%${DIR}txid272634/ERR3672192_2.fastq,${DIR}txid272634/ERR3672193_1.fastq%${DIR}txid272634/ERR3672193_2.fastq -o ${DIR}txid272634/rh_outputs/txid272634 -g ${DIR}txid272634/txid272634

# ------------------ EVAL ------------------


# ------------------- TEST -------------------
# mkdir ${DIR}txid298386/txid298386/
# cp ${DIR}txid298386/txid298386.fasta ${DIR}txid298386/txid298386/txid298386.fna
# python 4_convert_gff3.py ${DIR}txid298386/txid298386.gff3 ${DIR}txid298386/txid298386/txid298386
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid298386/SRR500950.fastq,${DIR}txid298386/SRR500951.fastq -o ${DIR}txid298386/rh_outputs/txid298386 -g ${DIR}txid298386/txid298386

# mkdir ${DIR}txid176299/txid176299/
# cp ${DIR}txid176299/txid176299.fasta ${DIR}txid176299/txid176299/txid176299.fna
# python 4_convert_gff3.py ${DIR}txid176299/txid176299.gff3 ${DIR}txid176299/txid176299/txid176299
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid176299/SRR14432343.fastq,${DIR}txid176299/SRR14432344.fastq,${DIR}txid176299/SRR14432345.fastq -o ${DIR}txid176299/rh_outputs/txid176299 -g ${DIR}txid176299/txid176299

# mkdir ${DIR}txid224326/txid224326/
# cp ${DIR}txid224326/txid224326.fasta ${DIR}txid224326/txid224326/txid224326.fna
# python 4_convert_gff3.py ${DIR}txid224326/txid224326.gff3 ${DIR}txid224326/txid224326/txid224326
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid224326/SRR11997800.fastq,${DIR}txid224326/SRR11997801.fastq,${DIR}txid224326/SRR11997802.fastq -o ${DIR}txid224326/rh_outputs/txid224326 -g ${DIR}txid224326/txid224326

# mkdir ${DIR}txid224911/txid224911/
# cp ${DIR}txid224911/txid224911.fasta ${DIR}txid224911/txid224911/txid224911.fna
# python 4_convert_gff3.py ${DIR}txid224911/txid224911.gff3 ${DIR}txid224911/txid224911/txid224911
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid224911/SRR13238987.fastq,${DIR}txid224911/SRR13238988.fastq,${DIR}txid224911/SRR13238989.fastq -o ${DIR}txid224911/rh_outputs/txid224911 -g ${DIR}txid224911/txid224911

# mkdir ${DIR}txid208964/txid208964/
# cp ${DIR}txid208964/txid208964.fasta ${DIR}txid208964/txid208964/txid208964.fna
# python 4_convert_gff3.py ${DIR}txid208964/txid208964.gff3 ${DIR}txid208964/txid208964/txid208964
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid208964/SRR11998427_1.fastq%${DIR}txid208964/SRR11998427_2.fastq,${DIR}txid208964/SRR11998428_1.fastq%${DIR}txid208964/SRR11998428_2.fastq,${DIR}txid208964/SRR11998429_1.fastq%${DIR}txid208964/SRR11998429_2.fastq -o ${DIR}txid208964/rh_outputs/txid208964 -g ${DIR}txid208964/txid208964

# mkdir ${DIR}txid214092/txid214092/
# cp ${DIR}txid214092/txid214092.fasta ${DIR}txid214092/txid214092/txid214092.fna
# python 4_convert_gff3.py ${DIR}txid214092/txid214092.gff3 ${DIR}txid214092/txid214092/txid214092
# java -Xmx1200m -cp Rockhopper.jar Rockhopper ${DIR}txid214092/SRR5489122.fastq,${DIR}txid214092/SRR5489125.fastq -o ${DIR}txid214092/rh_outputs/txid214092 -g ${DIR}txid214092/txid214092

# mkdir ${DIR}txid6239/txid6239/
# cp ${DIR}txid6239/txid6239.fasta ${DIR}txid6239/txid6239/txid6239.fna
# python 4_convert_gff3.py ${DIR}txid6239/txid6239.gff3 ${DIR}txid6239/txid6239/txid6239
unset JAVA_TOOL_OPTIONS
java -Xmx32g -cp Rockhopper.jar Rockhopper ${DIR}txid6239/SRR11605370.fastq,${DIR}txid6239/SRR11605378.fastq,${DIR}txid6239/SRR11605385.fastq -o ${DIR}txid6239/rh_outputs/txid6239 -g ${DIR}txid6239/txid6239

# ------------------- EVAL -------------------