#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=00:10:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4

module load python
source ../4_data_process/env/bin/activate

# ---------- training ----------
# python 5_map.py txid224308
# python 5_map.py txid196627
# python 5_map.py txid511145
# python 5_map_hp.py txid85962
# python 5_map.py txid297246
# python 5_map.py txid169963
# python 5_map.py txid272634

# ---------- eval ----------
python 5_of_eval.py txid224308
python 5_of_eval.py txid196627
python 5_of_eval.py txid511145
python 5_of_eval.py txid85962
python 5_of_eval.py txid297246
python 5_of_eval.py txid169963
python 5_of_eval.py txid272634

# ---------- testing ----------
# python 5_map.py txid298386
# python 5_map.py txid176299
# python 5_map.py txid224326
# # python 5_map.py txid224911 # not in website
# python 5_map.py txid208964
# # python 5_map.py txid214092 # no prediction
# # python 5_map.py txid6239 # not in website

# ---------- eval ----------
python 5_of_eval.py txid298386
python 5_of_eval.py txid176299
python 5_of_eval.py txid224326
# python 5_of_eval.py txid224911 # not in website
python 5_of_eval.py txid208964
# python 5_of_eval.py txid214092 # no prediction
# python 5_of_eval.py txid6239 # not in website


