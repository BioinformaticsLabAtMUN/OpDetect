#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=01:00:00
#SBATCH --mem=64G

module load python/3.10.13
source ../4_data_process/envr/bin/activate

# -------------Train organisms, all but one---------------- To train unbiased models, and then test on the left-out organism
python ../4_data_process/integrate.py txid196627,txid511145,txid85962,txid297246,txid169963,txid272634 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train_but_one/data_integrated_txid224308.pkl
python ../4_data_process/process.py ../0_data/TEST/train_but_one data_integrated_txid224308.pkl data_processed_txid224308.npz TEST

python ../4_data_process/integrate.py txid224308,txid511145,txid85962,txid297246,txid169963,txid272634 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train_but_one/data_integrated_txid196627.pkl
python ../4_data_process/process.py ../0_data/TEST/train_but_one data_integrated_txid196627.pkl data_processed_txid196627.npz TEST

python ../4_data_process/integrate.py txid224308,txid196627,txid85962,txid297246,txid169963,txid272634 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train_but_one/data_integrated_txid511145.pkl
python ../4_data_process/process.py ../0_data/TEST/train_but_one data_integrated_txid511145.pkl data_processed_txid511145.npz TEST

python ../4_data_process/integrate.py txid224308,txid196627,txid511145,txid297246,txid169963,txid272634 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train_but_one/data_integrated_txid85962.pkl
python ../4_data_process/process.py ../0_data/TEST/train_but_one data_integrated_txid85962.pkl data_processed_txid85962.npz TEST

python ../4_data_process/integrate.py txid224308,txid196627,txid511145,txid85962,txid169963,txid272634 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train_but_one/data_integrated_txid297246.pkl
python ../4_data_process/process.py ../0_data/TEST/train_but_one data_integrated_txid297246.pkl data_processed_txid297246.npz TEST

python ../4_data_process/integrate.py txid224308,txid196627,txid511145,txid85962,txid297246,txid272634 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train_but_one/data_integrated_txid169963.pkl
python ../4_data_process/process.py ../0_data/TEST/train_but_one data_integrated_txid169963.pkl data_processed_txid169963.npz TEST

python ../4_data_process/integrate.py txid224308,txid196627,txid511145,txid85962,txid297246,txid169963 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train_but_one/data_integrated_txid272634.pkl
python ../4_data_process/process.py ../0_data/TEST/train_but_one data_integrated_txid272634.pkl data_processed_txid272634.npz TEST


# ------------------Train organisms, individually------------------ To test the performance of the model trained on all but one organism, and the original model.
python ../4_data_process/integrate.py txid224308 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train/data_integrated_txid224308.pkl
python ../4_data_process/process.py ../0_data/TEST/train data_integrated_txid224308.pkl data_processed_txid224308.npz TEST

python ../4_data_process/integrate.py txid196627 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train/data_integrated_txid196627.pkl
python ../4_data_process/process.py ../0_data/TEST/train data_integrated_txid196627.pkl data_processed_txid196627.npz TEST

python ../4_data_process/integrate.py txid511145 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train/data_integrated_txid511145.pkl
python ../4_data_process/process.py ../0_data/TEST/train data_integrated_txid511145.pkl data_processed_txid511145.npz TEST

python ../4_data_process/integrate.py txid85962 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train/data_integrated_txid85962.pkl
python ../4_data_process/process.py ../0_data/TEST/train data_integrated_txid85962.pkl data_processed_txid85962.npz TEST

python ../4_data_process/integrate.py txid297246 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train/data_integrated_txid297246.pkl
python ../4_data_process/process.py ../0_data/TEST/train data_integrated_txid297246.pkl data_processed_txid297246.npz TEST

python ../4_data_process/integrate.py txid169963 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train/data_integrated_txid169963.pkl
python ../4_data_process/process.py ../0_data/TEST/train data_integrated_txid169963.pkl data_processed_txid169963.npz TEST

python ../4_data_process/integrate.py txid272634 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/train/data_integrated_txid272634.pkl
python ../4_data_process/process.py ../0_data/TEST/train data_integrated_txid272634.pkl data_processed_txid272634.npz TEST


# -------------------Test organisms, individually-------------------
python ../4_data_process/integrate.py txid298386 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/test/data_integrated_.pkl
python ../4_data_process/process.py ../0_data/TEST/test data_integrated_.pkl data_processed_txid298386.npz TEST

python ../4_data_process/integrate.py txid176299 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/test/data_integrated_.pkl
python ../4_data_process/process.py ../0_data/TEST/test data_integrated_.pkl data_processed_txid176299.npz TEST

python ../4_data_process/integrate.py txid224326 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/test/data_integrated_.pkl
python ../4_data_process/process.py ../0_data/TEST/test data_integrated_.pkl data_processed_txid224326.npz TEST

python ../4_data_process/integrate.py txid224911 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/test/data_integrated_.pkl
python ../4_data_process/process.py ../0_data/TEST/test data_integrated_.pkl data_processed_txid224911.npz TEST

python ../4_data_process/integrate.py txid208964 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/test/data_integrated_.pkl
python ../4_data_process/process.py ../0_data/TEST/test data_integrated_.pkl data_processed_txid208964.npz TEST

python ../4_data_process/integrate.py txid214092 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/test/data_integrated_.pkl
python ../4_data_process/process.py ../0_data/TEST/test data_integrated_.pkl data_processed_txid214092.npz TEST

python ../4_data_process/integrate.py txid6239 ../0_data gene_annotation.bed base_cov labels ../0_data/TEST/test/data_integrated_.pkl
python ../4_data_process/process.py ../0_data/TEST/test data_integrated_.pkl data_processed_txid6239.npz TEST