#!/bin/bash
#SBATCH --account=def-lpenacas
#SBATCH --time=3:00:00
#SBATCH --mem=64G
#SBATCH --cpus-per-task=4

module load python
source ../4_data_process/env/bin/activate

python baseline.py hyp.json data_processed.npz