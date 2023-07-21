#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=00:20:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4

module load python
source ../4_data_process/env/bin/activate

# -------------TEST----------------

# python roc.py txid298386
# # python roc.py txid176299
# # python roc.py txid224326
# # python roc.py txid224911
# # python roc.py txid208964
# # python roc.py txid214092
# python roc.py txid6239

# -------------TRAIN----------------
python roc.py txid224308
python roc.py txid196627 
python roc.py txid511145
python roc.py txid85962 
python roc.py txid297246 
python roc.py txid169963
python roc.py txid272634
