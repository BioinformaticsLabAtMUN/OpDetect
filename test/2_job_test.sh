#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=2:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4

module load python
source ../4_data_process/env/bin/activate

# without excluding the test org:
# ------------------ Train ------------------
python 2_baseline.py 2_hyp_test.json txid224308/gene_pairs.csv data_txid224308_test.npz
python 2_baseline.py 2_hyp_test.json txid196627/gene_pairs.csv data_txid196627_test.npz
python 2_baseline.py 2_hyp_test.json txid511145/gene_pairs.csv data_txid511145_test.npz
python 2_baseline.py 2_hyp_test.json txid85962/gene_pairs.csv data_txid85962_test.npz
python 2_baseline.py 2_hyp_test.json txid297246/gene_pairs.csv data_txid297246_test.npz
python 2_baseline.py 2_hyp_test.json txid169963/gene_pairs.csv data_txid169963_test.npz
python 2_baseline.py 2_hyp_test.json txid272634/gene_pairs.csv data_txid272634_test.npz

# ------------------- TEST -------------------
python 2_baseline.py 2_hyp_test.json txid298386/gene_pairs.csv data_txid298386_test.npz
python 2_baseline.py 2_hyp_test.json txid176299/gene_pairs.csv data_txid176299_test.npz
python 2_baseline.py 2_hyp_test.json txid224326/gene_pairs.csv data_txid224326_test.npz
python 2_baseline.py 2_hyp_test.json txid224911/gene_pairs.csv data_txid224911_test.npz
python 2_baseline.py 2_hyp_test.json txid208964/gene_pairs.csv data_txid208964_test.npz
python 2_baseline.py 2_hyp_test.json txid214092/gene_pairs.csv data_txid214092_test.npz
python 2_baseline.py 2_hyp_test.json txid6239/gene_pairs.csv data_txid6239_test.npz

# # FUTURE WORK:
# # ------------------ Train ------------------
# python 2_baseline.py 2_hyp_test.json txid224308/gene_pairs.csv data_txid224308.npz
# python 2_baseline.py 2_hyp_test.json txid196627/gene_pairs.csv data_txid196627.npz
# python 2_baseline.py 2_hyp_test.json txid511145/gene_pairs.csv data_txid511145.npz
# python 2_baseline.py 2_hyp_test.json txid85962/gene_pairs.csv data_txid85962.npz
# python 2_baseline.py 2_hyp_test.json txid297246/gene_pairs.csv data_txid297246.npz
# python 2_baseline.py 2_hyp_test.json txid169963/gene_pairs.csv data_txid169963.npz
# python 2_baseline.py 2_hyp_test.json txid272634/gene_pairs.csv data_txid272634.npz

# # ------------------- TEST -------------------
# python 2_baseline.py 2_hyp_test.json txid298386/gene_pairs.csv data_txid298386.npz
# python 2_baseline.py 2_hyp_test.json txid176299/gene_pairs.csv data_txid176299.npz
# python 2_baseline.py 2_hyp_test.json txid224326/gene_pairs.csv data_txid224326.npz
# python 2_baseline.py 2_hyp_test.json txid224911/gene_pairs.csv data_txid224911.npz
# python 2_baseline.py 2_hyp_test.json txid208964/gene_pairs.csv data_txid208964.npz
# python 2_baseline.py 2_hyp_test.json txid214092/gene_pairs.csv data_txid214092.npz
# python 2_baseline.py 2_hyp_test.json txid6239/gene_pairs.csv data_txid6239.npz
