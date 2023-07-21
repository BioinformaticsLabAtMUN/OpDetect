#!/bin/bash

Help()
{
   # Display Help
   echo "SynDIR: scriptTemplate [-r|d|l]"
   echo "options:"
   echo "r     RNA-seq access codes separated by ','."
   echo "d     Directory"
   echo "l     Layout, P for Paired or S for Single."
}

while getopts r:d:l: flag
do
    case "${flag}" in
        d) DIR=${OPTARG};;
        r) IFS=',' read -r -a RNA <<< ${OPTARG};;
        l) LAYOUT=${OPTARG};;
        \?) Help exit;;
    esac
done

for ACC in "${RNA[@]}"
do

	echo ${DIR}
	
	if [[ ${LAYOUT} = "P" ]]
	then
		mkdir ${DIR}/qc
		fastp -i ${DIR}/${ACC}_1.fastq -I ${DIR}/${ACC}_2.fastq -o ${DIR}/qc/${ACC}_1.fastq -O ${DIR}/qc/${ACC}_2.fastq -h ${DIR}/qc/${ACC}.html -5 --cut_front_window_size 1 --cut_front_mean_quality 3 -r --cut_right_window_size 4 --cut_right_mean_quality 15
	else
		mkdir ${DIR}/qc
		fastp -i ${DIR}/${ACC}.fastq -o ${DIR}/qc/${ACC}.fastq -h ${DIR}/qc/${ACC}.html -5  --cut_front_window_size 1 --cut_front_mean_quality 3 -r --cut_right_window_size 4 --cut_right_mean_quality 15
	fi
done
