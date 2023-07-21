#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=12:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4

module load python
source ../4_data_process/env/bin/activate

# ------------------ Train ------------------
python ../5_model/baseline.py 2_hyp_train.json data_processed_w_txid224308.npz
python 2_baseline.py 2_hyp_train.json txid224308/gene_pairs.csv data_txid224308_test.npz

python ../5_model/baseline.py 2_hyp_train.json data_processed_w_txid196627.npz
python 2_baseline.py 2_hyp_train.json txid196627/gene_pairs.csv data_txid196627_test.npz

python ../5_model/baseline.py 2_hyp_train.json data_processed_w_txid511145.npz
python 2_baseline.py 2_hyp_train.json txid511145/gene_pairs.csv data_txid511145_test.npz

python ../5_model/baseline.py 2_hyp_train.json data_processed_w_txid85962.npz
python 2_baseline.py 2_hyp_train.json txid85962/gene_pairs.csv data_txid85962_test.npz

python ../5_model/baseline.py 2_hyp_train.json data_processed_w_txid297246.npz
python 2_baseline.py 2_hyp_train.json txid297246/gene_pairs.csv data_txid297246_test.npz

python ../5_model/baseline.py 2_hyp_train.json data_processed_w_txid169963.npz
python 2_baseline.py 2_hyp_train.json txid169963/gene_pairs.csv data_txid169963_test.npz

python ../5_model/baseline.py 2_hyp_train.json data_processed_w_txid272634.npz
python 2_baseline.py 2_hyp_train.json txid272634/gene_pairs.csv data_txid272634_test.npz
