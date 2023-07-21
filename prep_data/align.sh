#!/bin/bash

Help()
{
   # Display Help
   echo "Syntax: scriptTemplate [-r|d|l|q|f]"
   echo "options:"
   echo "r     RNA-seq access codes separated by ','."
   echo "d     Directory"
   echo "l     Layout, P for Paired or S for Single."
   echo "q     Quality Control, Y or N."
   echo "f	   Fasta file name"
}

while getopts r:d:l:q:f: flag
do
    case "${flag}" in
        d) DIR=${OPTARG};;
        r) IFS=',' read -r -a RNA <<< ${OPTARG};;
        l) LAYOUT=${OPTARG};;
		q) QC=${OPTARG};;
		f) FASTA=${OPTARG};;
        \?) Help exit;;
    esac
done

#build hisat2 index:
mkdir ${DIR}/index
hisat2-build -p 16 ${DIR}/${FASTA} ${DIR}/index/index -q

for ACC in "${RNA[@]}"
do
	
	if [[ ${LAYOUT} = "P" ]]
	then
		echo "start align" ${ACC}

		# with qc
		if [[ ${QC} = "Y" ]]
		then
			hisat2 -p 8 -x ${DIR}/index/index -1 ${DIR}/qc/${ACC}_1.fastq -2 ${DIR}/qc/${ACC}_2.fastq -S ${DIR}/aligned.sam
		
		# without qc
		else
			hisat2 -p 8 -x ${DIR}/index/index -1 ${DIR}/${ACC}_1.fastq -2 ${DIR}/${ACC}_2.fastq -S ${DIR}/aligned.sam
		fi
	
	else
		echo "start align" ${ACC}

		# with qc
		if [[ ${QC} = "Y" ]]
		then
			hisat2 -p 8 -x ${DIR}/index/index -U ${DIR}/qc/${ACC}.fastq -S ${DIR}/aligned.sam
		
		# without qc
		else
			hisat2 -p 8 -x ${DIR}/index/index -U ${DIR}/${ACC}.fastq -S ${DIR}/aligned.sam
		fi
		
	fi
	
	#Convert sam file to bam and sort it
	samtools view -b -o ${DIR}/aligned.bam ${DIR}/aligned.sam

	samtools sort ${DIR}/aligned.bam -o ${DIR}/aligned_sorted.bam

	samtools index ${DIR}/aligned_sorted.bam

	#Per-base gene coverage
	bedtools genomecov -d -ibam ${DIR}/aligned_sorted.bam > ${DIR}/base_cov_${ACC}

done

rm ${DIR}/aligned.sam
rm ${DIR}/aligned.bam
rm ${DIR}/aligned_sorted.bam