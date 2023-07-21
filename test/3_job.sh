#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=00:10:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4

module load python
source ../4_data_process/env/bin/activate

# ---------- training ----------
# python 3_map.py txid224308
# python 3_map.py txid196627
# python 3_map.py txid511145
# python 3_map.py txid85962
# python 3_map.py txid297246
# python 3_map.py txid169963
# python 3_map.py txid272634

# ---------- eval ----------
python 3_om_eval.py txid224308
python 3_om_eval.py txid196627
python 3_om_eval.py txid511145
python 3_om_eval.py txid85962
python 3_om_eval.py txid297246
python 3_om_eval.py txid169963
python 3_om_eval.py txid272634

# ---------- testing ----------
# python 3_map.py txid298386 
# python 3_map.py txid176299
# python 3_map.py txid224326
# python 3_map.py txid224911
# python 3_map.py txid208964
# python 3_map.py txid214092
# python 3_map.py txid6239 #no pred

# ---------- eval ----------
python 3_om_eval.py txid298386 
python 3_om_eval.py txid176299
python 3_om_eval.py txid224326
python 3_om_eval.py txid224911
python 3_om_eval.py txid208964
python 3_om_eval.py txid214092
# python 3_om_eval.py txid6239
