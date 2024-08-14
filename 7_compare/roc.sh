#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=00:10:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4

module load python
source ../4_data_process/env/bin/activate

# -------------TEST----------------

python roc.py txid298386
python roc.py txid6239

# -------------TRAIN----------------
python roc.py txid224308 NE
python roc.py txid196627 NE
python roc.py txid511145 NE
python roc.py txid85962 NE
python roc.py txid297246 NE
python roc.py txid169963 NE
python roc.py txid272634 NE
