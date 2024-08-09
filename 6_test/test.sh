#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=01:00:00
#SBATCH --mem=64G

module load python
source ../5_train/env/bin/activate

# -------------------Test organisms, individually-------------------
# python test.py dir model_weights_path model_name test_data test_labels 
python test.py ../0_data models/versions OpDetect TEST/test/data_processed_txid298386.npz txid298386/gene_pairs.csv