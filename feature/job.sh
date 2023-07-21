#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=05:00:00
#SBATCH --mem=3G

module load python
# virtualenv --no-download $SLURM_TMPDIR/env
# source $SLURM_TMPDIR/env/bin/activate
# pip install --no-index --upgrade pip
# pip install --no-index -r requirements.txt

source env/bin/activate

# python integrate.py txid224308,txid196627,txid511145,txid85962,txid297246,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated.pkl

# python process.py ../../operons/data_odb data_integrated.pkl data_processed

python visualize.py ../../operons/data_odb data_processed_vis.pkl




# # -------------test----------------
# python integrate.py txid196627,txid511145,txid85962,txid297246,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid224308.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid224308.pkl data_processed_w_txid224308

# python integrate.py txid224308,txid511145,txid85962,txid297246,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid196627.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid196627.pkl data_processed_w_txid196627

# python integrate.py txid224308,txid196627,txid85962,txid297246,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid511145.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid511145.pkl data_processed_w_txid511145

# python integrate.py txid224308,txid196627,txid511145,txid297246,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid85962.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid85962.pkl data_processed_w_txid85962

# python integrate.py txid224308,txid196627,txid511145,txid85962,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid297246.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid297246.pkl data_processed_w_txid297246

# python integrate.py txid224308,txid196627,txid511145,txid85962,txid297246,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid169963.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid169963.pkl data_processed_w_txid169963

# python integrate.py txid224308,txid196627,txid511145,txid85962,txid297246,txid169963 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated_w_txid272634.pkl
# python process.py ../../operons/data_odb data_integrated_w_txid272634.pkl data_processed_w_txid272634

