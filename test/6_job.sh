#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=10:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4

# virtualenv --no-download operonSEQer_env
source operonSEQer_env/bin/activate
module load python/3.9.6

# pip install -r 6_os_req.txt

# ------------------ Train ------------------
python 6_os.py -t '../../operons/data_odb/txid224308/' -c base_cov_SRR15049591 -g gene_annotation.bed -o os_outputs/SRR15049591
python 6_os.py -t '../../operons/data_odb/txid224308/' -c base_cov_SRR15049592 -g gene_annotation.bed -o os_outputs/SRR15049592
python 6_os.py -t '../../operons/data_odb/txid224308/' -c base_cov_SRR15049593 -g gene_annotation.bed -o os_outputs/SRR15049593
python 6_os.py -t '../../operons/data_odb/txid224308/' -c base_cov_ERR6156944 -g gene_annotation.bed -o os_outputs/ERR6156944
python 6_os.py -t '../../operons/data_odb/txid224308/' -c base_cov_ERR6156945 -g gene_annotation.bed -o os_outputs/ERR6156945
python 6_os.py -t '../../operons/data_odb/txid224308/' -c base_cov_ERR6156946 -g gene_annotation.bed -o os_outputs/ERR6156946

python 6_os.py -t '../../operons/data_odb/txid196627/' -c base_cov_SRR7977557 -g gene_annotation.bed -o os_outputs/SRR7977557
python 6_os.py -t '../../operons/data_odb/txid196627/' -c base_cov_SRR7977561 -g gene_annotation.bed -o os_outputs/SRR7977561
python 6_os.py -t '../../operons/data_odb/txid196627/' -c base_cov_SRR7977565 -g gene_annotation.bed -o os_outputs/SRR7977565
python 6_os.py -t '../../operons/data_odb/txid196627/' -c base_cov_ERR3380462 -g gene_annotation.bed -o os_outputs/ERR3380462
python 6_os.py -t '../../operons/data_odb/txid196627/' -c base_cov_ERR3380465 -g gene_annotation.bed -o os_outputs/ERR3380465
python 6_os.py -t '../../operons/data_odb/txid196627/' -c base_cov_ERR3380468 -g gene_annotation.bed -o os_outputs/ERR3380468

python 6_os.py -t '../../operons/data_odb/txid511145/' -c base_cov_SRR1787590 -g gene_annotation.bed -o os_outputs/SRR1787590
python 6_os.py -t '../../operons/data_odb/txid511145/' -c base_cov_SRR1787592 -g gene_annotation.bed -o os_outputs/SRR1787592
python 6_os.py -t '../../operons/data_odb/txid511145/' -c base_cov_SRR1787594 -g gene_annotation.bed -o os_outputs/SRR1787594
python 6_os.py -t '../../operons/data_odb/txid511145/' -c base_cov_SRR7217927 -g gene_annotation.bed -o os_outputs/SRR7217927
python 6_os.py -t '../../operons/data_odb/txid511145/' -c base_cov_SRR7217928 -g gene_annotation.bed -o os_outputs/SRR7217928
python 6_os.py -t '../../operons/data_odb/txid511145/' -c base_cov_SRR7217929 -g gene_annotation.bed -o os_outputs/SRR7217929

python 6_os.py -t '../../operons/data_odb/txid85962/' -c base_cov_SRR5217496 -g gene_annotation.bed -o os_outputs/SRR5217496

python 6_os.py -t '../../operons/data_odb/txid297246/' -c base_cov_ERR1157043 -g gene_annotation.bed -o os_outputs/ERR1157043
python 6_os.py -t '../../operons/data_odb/txid297246/' -c base_cov_ERR1157044 -g gene_annotation.bed -o os_outputs/ERR1157044
python 6_os.py -t '../../operons/data_odb/txid297246/' -c base_cov_ERR1157045 -g gene_annotation.bed -o os_outputs/ERR1157045

python 6_os.py -t '../../operons/data_odb/txid169963/' -c base_cov_SRR11998208 -g gene_annotation.bed -o os_outputs/SRR11998208
python 6_os.py -t '../../operons/data_odb/txid169963/' -c base_cov_SRR11998211 -g gene_annotation.bed -o os_outputs/SRR11998211
python 6_os.py -t '../../operons/data_odb/txid169963/' -c base_cov_SRR11998214 -g gene_annotation.bed -o os_outputs/SRR11998214
python 6_os.py -t '../../operons/data_odb/txid169963/' -c base_cov_SRR11998217 -g gene_annotation.bed -o os_outputs/SRR11998217
python 6_os.py -t '../../operons/data_odb/txid169963/' -c base_cov_SRR11998220 -g gene_annotation.bed -o os_outputs/SRR11998220
python 6_os.py -t '../../operons/data_odb/txid169963/' -c base_cov_SRR11998223 -g gene_annotation.bed -o os_outputs/SRR11998223

python 6_os.py -t '../../operons/data_odb/txid272634/' -c base_cov_ERR3672190 -g gene_annotation.bed -o os_outputs/ERR3672190
python 6_os.py -t '../../operons/data_odb/txid272634/' -c base_cov_ERR3672191 -g gene_annotation.bed -o os_outputs/ERR3672191
python 6_os.py -t '../../operons/data_odb/txid272634/' -c base_cov_ERR3672192 -g gene_annotation.bed -o os_outputs/ERR3672192
python 6_os.py -t '../../operons/data_odb/txid272634/' -c base_cov_ERR3672193 -g gene_annotation.bed -o os_outputs/ERR3672193

# ------------------ EVAL ------------------

python 6_os_eval.py ../../operons/data_odb/txid224308 gene_pairs.csv SRR15049591,SRR15049592,SRR15049593,ERR6156944,ERR6156945,ERR6156946
python 6_os_eval.py ../../operons/data_odb/txid196627 gene_pairs.csv SRR7977557,SRR7977561,SRR7977565,ERR3380462,ERR3380465,ERR3380468
python 6_os_eval.py ../../operons/data_odb/txid511145 gene_pairs.csv SRR1787590,SRR1787592,SRR1787594,SRR7217927,SRR7217928,SRR7217929
python 6_os_eval.py ../../operons/data_odb/txid85962 gene_pairs.csv SRR5217496
python 6_os_eval.py ../../operons/data_odb/txid297246 gene_pairs.csv ERR1157043,ERR1157044,ERR1157045
python 6_os_eval.py ../../operons/data_odb/txid169963 gene_pairs.csv SRR11998208,SRR11998211,SRR11998214,SRR11998217,SRR11998220,SRR11998223
python 6_os_eval.py ../../operons/data_odb/txid272634 gene_pairs.csv ERR3672190,ERR3672191,ERR3672192,ERR3672193

# ------------------- TEST -------------------
python 6_os.py -t '../../operons/data_odb/txid298386/' -c base_cov_SRR500950 -g gene_annotation.bed -o os_outputs/SRR500950
python 6_os.py -t '../../operons/data_odb/txid298386/' -c base_cov_SRR500951 -g gene_annotation.bed -o os_outputs/SRR500951

python 6_os.py -t '../../operons/data_odb/txid176299/' -c base_cov_SRR14432343 -g gene_annotation.bed -o os_outputs/SRR14432343
python 6_os.py -t '../../operons/data_odb/txid176299/' -c base_cov_SRR14432344 -g gene_annotation.bed -o os_outputs/SRR14432344
python 6_os.py -t '../../operons/data_odb/txid176299/' -c base_cov_SRR14432345 -g gene_annotation.bed -o os_outputs/SRR14432345

python 6_os.py -t '../../operons/data_odb/txid224326/' -c base_cov_SRR11997800 -g gene_annotation.bed -o os_outputs/SRR11997800
python 6_os.py -t '../../operons/data_odb/txid224326/' -c base_cov_SRR11997801 -g gene_annotation.bed -o os_outputs/SRR11997801
python 6_os.py -t '../../operons/data_odb/txid224326/' -c base_cov_SRR11997802 -g gene_annotation.bed -o os_outputs/SRR11997802

python 6_os.py -t '../../operons/data_odb/txid224911/' -c base_cov_SRR13238987 -g gene_annotation.bed -o os_outputs/SRR13238987
python 6_os.py -t '../../operons/data_odb/txid224911/' -c base_cov_SRR13238988 -g gene_annotation.bed -o os_outputs/SRR13238988
python 6_os.py -t '../../operons/data_odb/txid224911/' -c base_cov_SRR13238989 -g gene_annotation.bed -o os_outputs/SRR13238989

python 6_os.py -t '../../operons/data_odb/txid208964/' -c base_cov_SRR11998427 -g gene_annotation.bed -o os_outputs/SRR11998427
python 6_os.py -t '../../operons/data_odb/txid208964/' -c base_cov_SRR11998428 -g gene_annotation.bed -o os_outputs/SRR11998428
python 6_os.py -t '../../operons/data_odb/txid208964/' -c base_cov_SRR11998429 -g gene_annotation.bed -o os_outputs/SRR11998429

python 6_os.py -t '../../operons/data_odb/txid214092/' -c base_cov_SRR5489122 -g gene_annotation.bed -o os_outputs/SRR5489122
python 6_os.py -t '../../operons/data_odb/txid214092/' -c base_cov_SRR5489125 -g gene_annotation.bed -o os_outputs/SRR5489125

python 6_os.py -t '../../operons/data_odb/txid6239/' -c base_cov_SRR11605370 -g gene_annotation.bed -o os_outputs/SRR11605370
python 6_os.py -t '../../operons/data_odb/txid6239/' -c base_cov_SRR11605378 -g gene_annotation.bed -o os_outputs/SRR11605378
python 6_os.py -t '../../operons/data_odb/txid6239/' -c base_cov_SRR11605385 -g gene_annotation.bed -o os_outputs/SRR11605385

# ------------------- EVAL -------------------
python 6_os_eval.py ../../operons/data_odb/txid298386 gene_pairs.csv SRR500950,SRR500951
python 6_os_eval.py ../../operons/data_odb/txid176299 gene_pairs.csv SRR14432343,SRR14432344,SRR14432345
python 6_os_eval.py ../../operons/data_odb/txid224326 gene_pairs.csv SRR11997800,SRR11997801,SRR11997802
python 6_os_eval.py ../../operons/data_odb/txid224911 gene_pairs.csv SRR13238987,SRR13238988,SRR13238989
python 6_os_eval.py ../../operons/data_odb/txid208964 gene_pairs.csv SRR11998427,SRR11998428,SRR11998429
python 6_os_eval.py ../../operons/data_odb/txid214092 gene_pairs.csv SRR5489122,SRR5489125
python 6_os_eval.py ../../operons/data_odb/txid6239 gene_pairs.csv SRR11605370,SRR11605378,SRR11605385


