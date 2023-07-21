#!/bin/bash

Help()
{
   # Display Help
   echo "Syntax: scriptTemplate [-r|t|o]"
   echo "options:"
   echo "r     RNA-seq access codes separated by ','."
   echo "t     Taxonomy access code of organism(just number)."
   echo "o     Output directory."
}

while getopts t:r:o flag
do
    case "${flag}" in
        t) TAX=${OPTARG};;
        r) IFS=',' read -r -a RNA <<< ${OPTARG};;
        o) DIR=${OPTARG};;
        \?) Help exit;;
    esac
done

mkdir ${DIR}txid${TAX}

for ACC in "${RNA[@]}"
do
	
	prefetch ${ACC}
	fasterq-dump ${ACC} -O ${DIR}txid${TAX}/

done