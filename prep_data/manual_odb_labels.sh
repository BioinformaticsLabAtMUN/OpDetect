#!/bin/bash
TAX=224308
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;old_locus_tag=(\w+).*/$1/g'| perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g' | perl -pe 's/(.*\t\w*)_(.*)/$1$2/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=196627
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=511145
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g' | awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=85962
awk -F "\t" '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID=gene:(\w+);.*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g' | perl -pe 's/(.*\t\w*)_(.*)/$1$2/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=297246
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=169963
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed
# python3 ../../operons/data_odb/txid${TAX}/fix_names.py

TAX=272634
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;old_locus_tag=(\w+).*/$1/g' | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g'| perl -pe 's/\s([^\n])/\t$1/g' | perl -pe 's/(.*\t\w*)_(.*)/$1$2/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=298386
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}_1.gff3 | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation_1.bed
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}_2.gff3 | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation_2.bed
cat ../../operons/data_odb/txid${TAX}/gene_annotation_1.bed ../../operons/data_odb/txid${TAX}/gene_annotation_2.bed > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=176299
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}_1.gff3 | perl -pe 's/ID.*;old_locus_tag=.*(.{7})/$1/g' | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation_1.bed
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}_2.gff3 | perl -pe 's/ID.*;old_locus_tag=.*(.{7})/$1/g' | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation_2.bed
cat ../../operons/data_odb/txid${TAX}/gene_annotation_1.bed ../../operons/data_odb/txid${TAX}/gene_annotation_2.bed > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=224326
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;old_locus_tag=(\w+).*/$1/g'| perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g' | awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=224911
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;old_locus_tag=(\w+).*/$1/g'| perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g' | awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=208964
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=214092
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;old_locus_tag=(\w+).*/$1/g'| perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g' | awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=6239
awk -F "\t"  '{if ($2=='${TAX}') {print $4}}' ../../operons/data_odb/odb4_labels > ../../operons/data_odb/txid${TAX}/labels
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}_1.gff3 | perl -pe 's/ID.*;locus_tag=([^\n;]+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation_1.bed
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}_2.gff3 | perl -pe 's/ID.*;locus_tag=([^\n;]+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation_2.bed
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}_3.gff3 | perl -pe 's/ID.*;locus_tag=([^\n;]+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation_3.bed
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}_4.gff3 | perl -pe 's/ID.*;locus_tag=([^\n;]+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation_4.bed
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}_5.gff3 | perl -pe 's/ID.*;locus_tag=([^\n;]+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation_5.bed
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}_6.gff3 | perl -pe 's/ID.*;locus_tag=([^\n;]+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation_6.bed
cat ../../operons/data_odb/txid${TAX}/gene_annotation_*.bed > ../../operons/data_odb/txid${TAX}/gene_annotation.bed

TAX=272942
awk '{if ($3=="gene") {print}}' ../../operons/data_odb/txid${TAX}/txid${TAX}.gff3 | perl -pe 's/ID.*;locus_tag=(\w+).*/$1/g' | perl -pe 's/\s([^\n])/\t$1/g'| awk '{OFS="\t"; print $1,$2,$3,$4,$5,$6,$7,$8,$9}' > ../../operons/data_odb/txid${TAX}/gene_annotation.bed
