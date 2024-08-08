#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=20:00:00
#SBATCH --mem=128G

module load python/3.10.13
# virtualenv --no-download envr
# source envr/bin/activate
# pip install --no-index --upgrade pip
# pip install --no-index -r requirements.txt

source envr/bin/activate

# python integrate.py txid224308,txid196627,txid511145,txid85962,txid297246,txid169963,txid272634 ../0_data gene_annotation.bed base_cov labels ../0_data/data_integrated.pkl

python process.py ../0_data data_integrated.pkl data_processed_.npz VIS



# # -------------test----------------
# python integrate.py txid196627,txid511145,txid85962,txid297246,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid224308.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid224308.pkl data_processed_w_txid224308 TEST

# python integrate.py txid224308,txid511145,txid85962,txid297246,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid196627.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid196627.pkl data_processed_w_txid196627 TEST

# python integrate.py txid224308,txid196627,txid85962,txid297246,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid511145.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid511145.pkl data_processed_w_txid511145 TEST

# python integrate.py txid224308,txid196627,txid511145,txid297246,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid85962.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid85962.pkl data_processed_w_txid85962 TEST
# python integrate.py txid224308,txid196627,txid511145,txid85962,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid297246.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid297246.pkl data_processed_w_txid297246 TEST

# python integrate.py txid224308,txid196627,txid511145,txid85962,txid297246,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid169963.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid169963.pkl data_processed_w_txid169963 TEST

# python integrate.py txid224308,txid196627,txid511145,txid85962,txid297246,txid169963 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid272634.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid272634.pkl data_processed_w_txid272634 TEST

