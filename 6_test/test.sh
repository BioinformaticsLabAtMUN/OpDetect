#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=20:10:00
#SBATCH --mem=64G

module load python
source ../5_train/env/bin/activate
# python test.py dir model_weights_path model_name test_data test_labels 

# ------------------Train organisms, individually------------------ To test the performance of the model trained on all but one organism, and the original model.
python test.py ../0_data models/versions OpDetect TEST/train/data_processed_txid224308.npz txid224308/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/train/data_processed_txid196627.npz txid196627/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/train/data_processed_txid511145.npz txid511145/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/train/data_processed_txid85962.npz txid85962/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/train/data_processed_txid297246.npz txid297246/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/train/data_processed_txid169963.npz txid169963/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/train/data_processed_txid272634.npz txid272634/gene_pairs.csv


# -------------------Test organisms, individually-------------------
python test.py ../0_data models/versions OpDetect TEST/test/data_processed_txid298386.npz txid298386/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/test/data_processed_txid176299.npz txid176299/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/test/data_processed_txid224326.npz txid224326/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/test/data_processed_txid224911.npz txid224911/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/test/data_processed_txid208964.npz txid208964/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/test/data_processed_txid214092.npz txid214092/gene_pairs.csv

python test.py ../0_data models/versions OpDetect TEST/test/data_processed_txid6239.npz txid6239/gene_pairs.csv


# -------------Train organisms, all but one---------------- To train unbiased models, and then test on the left-out organism
python ../5_train/model.py ../5_train/hyp.json OpDetect_txid224308 TEST/train_but_one/data_processed_txid224308.npz
python test.py ../0_data models/versions OpDetect_txid224308 TEST/train_but_one/data_processed_txid224308.npz txid224308/gene_pairs.csv

python ../5_train/model.py ../5_train/hyp.json OpDetect_txid196627 TEST/train_but_one/data_processed_txid196627.npz
python test.py ../0_data models/versions OpDetect_txid196627 TEST/train_but_one/data_processed_txid196627.npz txid196627/gene_pairs.csv

python ../5_train/model.py ../5_train/hyp.json OpDetect_txid511145 TEST/train_but_one/data_processed_txid511145.npz
python test.py ../0_data models/versions OpDetect_txid511145 TEST/train_but_one/data_processed_txid511145.npz txid511145/gene_pairs.csv

python ../5_train/model.py ../5_train/hyp.json OpDetect_txid85962 TEST/train_but_one/data_processed_txid85962.npz
python test.py ../0_data models/versions OpDetect_txid85962 TEST/train_but_one/data_processed_txid85962.npz txid85962/gene_pairs.csv

python ../5_train/model.py ../5_train/hyp.json OpDetect_txid297246 TEST/train_but_one/data_processed_txid297246.npz
python test.py ../0_data models/versions OpDetect_txid297246 TEST/train_but_one/data_processed_txid297246.npz txid297246/gene_pairs.csv

python ../5_train/model.py ../5_train/hyp.json OpDetect_txid169963 TEST/train_but_one/data_processed_txid169963.npz
python test.py ../0_data models/versions OpDetect_txid169963 TEST/train_but_one/data_processed_txid169963.npz txid169963/gene_pairs.csv

python ../5_train/model.py ../5_train/hyp.json OpDetect_txid272634 TEST/train_but_one/data_processed_txid272634.npz
python test.py ../0_data models/versions OpDetect_txid272634 TEST/train_but_one/data_processed_txid272634.npz txid272634/gene_pairs.csv
