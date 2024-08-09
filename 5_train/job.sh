#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=2:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4

module load python
source env/bin/activate

python model.py hyp.json OpDetect data_processed.npz