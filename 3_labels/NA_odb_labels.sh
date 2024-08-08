#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=00:02:00
#SBATCH --mem=1G
 
module load bedtools

bash odb_labels.sh -d ../../operons/data_odb -t 224308 -n old_locus_tag=
# bash odb_labels.sh -d ../../operons/data_odb -t 196627 -n locus_tag=
bash odb_labels.sh -d ../../operons/data_odb -t 511145 -n locus_tag=
# bash odb_labels.sh -d ../../operons/data_odb -t 85962 -n gene_id=
# bash odb_labels.sh -d ../../operons/data_odb -t 297246 -n locus_tag=
bash odb_labels.sh -d ../../operons/data_odb -t 169963 -n locus_tag=
bash odb_labels.sh -d ../../operons/data_odb -t 272634 -n old_locus_tag=
bash odb_labels.sh -d ../../operons/data_odb -t 298386 -n locus_tag=
# bash odb_labels.sh -d ../../operons/data_odb -t 176299
# bash odb_labels.sh -d ../../operons/data_odb -t 224326
# bash odb_labels.sh -d ../../operons/data_odb -t 224911
# bash odb_labels.sh -d ../../operons/data_odb -t 208964
# bash odb_labels.sh -d ../../operons/data_odb -t 214092