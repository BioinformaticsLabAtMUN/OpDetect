#!/bin/bash

Help()
{
   # Display Help
   echo "Syntax: scriptTemplate [-d|t]"
   echo "options:"
   echo "d     Directory"
   echo "t     Taxonomy id"
   echo "n     Name of gene in labels"

}

while getopts d:t:n: flag
do
    case "${flag}" in
        d) DIR=${OPTARG};;
        t) TAX=${OPTARG};;
        n) NAME=${OPTARG};;
        \?) Help exit;;
    esac
done

awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ${DIR}/odb4_labels > ${DIR}/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ${DIR}/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*[;]?'${NAME}'[:-]?(\w+);.*/$1/g' | perl -pe 's/_//g'| perl -pe 's/\s([^\n])/\t$1/g' > ${DIR}/txid${TAX}/gene_annotation.bed


# if two chrs:
# txid243277
# awk '{if ($4 == "63") print > "mo_1.gff3"}' mo.gff3
# awk '{if ($4 == "64") print > "mo_2.gff3"}' mo.gff3
# cat gene_annotation_1.bed gene_annotation_2.bed > gene_annotation.bed
# txid272560
# awk '{if ($4 == "1898") print > "mo_1.gff3"}' mo.gff3
# awk '{if ($4 == "1899") print > "mo_2.gff3"}' mo.gff3
# cat gene_annotation_1.bed gene_annotation_2.bed > gene_annotation.bed