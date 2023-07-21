#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=01:00:00
#SBATCH --mem=64G

module load python
source ../4_data_process/env/bin/activate

# ------------------ Train ------------------
python ../4_data_process/integrate.py txid224308 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid224308 TEST

python ../4_data_process/integrate.py txid196627 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid196627 TEST

python ../4_data_process/integrate.py txid511145 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid511145 TEST

python ../4_data_process/integrate.py txid85962 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid85962 TEST

python ../4_data_process/integrate.py txid297246 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid297246 TEST

python ../4_data_process/integrate.py txid169963 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid169963 TEST

python ../4_data_process/integrate.py txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid272634 TEST


# ------------------- TEST -------------------
python ../4_data_process/integrate.py txid298386 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid298386 TEST

python ../4_data_process/integrate.py txid176299 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid176299 TEST

python ../4_data_process/integrate.py txid224326 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid224326 TEST

python ../4_data_process/integrate.py txid224911 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid224911 TEST

python ../4_data_process/integrate.py txid208964 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid208964 TEST

python ../4_data_process/integrate.py txid214092 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid214092 TEST

python ../4_data_process/integrate.py txid6239 ../../operons/data_odb gene_annotation.bed base_cov labels data.pkl TEST
python ../4_data_process/process.py ../../operons/data_odb data.pkl data_txid6239 TEST