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

python integrate.py txid224308,txid196627,txid511145,txid85962,txid297246,txid169963,txid272634 ../0_data gene_annotation.bed base_cov labels ../0_data/data_integrated.pkl

python process.py ../0_data data_integrated.pkl data_processed.npz VIS
