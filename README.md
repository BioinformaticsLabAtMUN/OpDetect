# OpDetect: A Deep Learning Tool for Operon Detection

## Overview

**OpDetect** is a convolutional and recurrent neural network-based tool designed to accurately and sensitively detect operons from RNA-seq data. Operons are groups of neighboring genes transcribed as a single mRNA unit, predominantly found in prokaryotic genomes. By leveraging RNA-seq data directly, OpDetect offers a species-agnostic approach that outperforms existing methods in terms of recall, F1-score, and AUROC.

---

## Key Features

- **Species-Agnostic**: Works across a wide range of bacterial species and can even detect operons in *Caenorhabditis elegans*, the only eukaryotic organism known to have operons.
- **Deep Learning Model**: Utilizes a CNN-LSTM architecture to capture spatial and sequential features from RNA-seq data.
- **Direct RNA-Seq Integration**: Does not rely on external databases, enabling application to a broader range of organisms.
- **Superior Performance**: Outperforms state-of-the-art tools like OperonMapper, Rockhopper, OperonSEQer, and OperonFinder.

---

## Installation

### Requirements

- Python 3.10+
- Required packages:
  - `numpy` (v1.24.4)
  - `pandas` (v2.1.0)
  - `matplotlib` (v3.8.4)
  - `scipy` (v1.10.1)
  - `tensorflow` (v2.16.1)
  - `scikit-learn` (v1.2.1)
  - `Orange3` (v3.30.0)

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-repo-name>/OpDetect.git
   cd OpDetect
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Data Preparation

1. **Prepare Data Directory**:

   - Create a subdirectory in `0_data` named with the `txid` of the organism (e.g., `txid12345`).
   - Place the following files in the subdirectory:
     - Read count files with names like `base_cov_SAMPLEID`.
     - Gene annotation file (e.g., `gene_annotation.bed`).
     - Labels file listing genes in the same operon on the same line.

2. **Process Data and Run Test**:
   From the main directory, execute the following commands:

   ```bash
   python 4_data_process/integrate.py txid12345 ../0_data gene_annotation.bed base_cov labels ../0_data/data_integrated.pkl
   ```

   - Replace `txid12345` with your organism-specific directory name.
   - Adjust paths to match your directory structure.

   ```bash
   python 4_data_process/process.py ../0_data data_integrated.pkl data_processed.npz TEST gene_pairs.csv
   ```

   - Outputs `gene_pairs.csv` containing gene-pair labels.

3. **Run Test**:

   ```bash
   python 6_test/test.py 0_data models/versions OpDetect data_processed_txid12345.npz txid12345/gene_pairs.csv
   ```

---

## Evaluation

### Metrics

- **Recall**
- **F1-score**
- **AUROC**

### Results

OpDetect consistently outperforms existing methods on validation organisms, achieving:

- Recall: 88.94%
- F1-score: 89.50%
- AUROC: 88.94%

---

## Citation

If you use OpDetect in your research, please cite:

Rezvan Karaji and Lourdes Peña-Castillo, "OpDetect: A Convolutional and Recurrent Neural Network Classifier for Precise and Sensitive Operon Detection from RNA-seq Data," *PLoS ONE*, 2024.

---

## Acknowledgments

This tool was developed at the Department of Computer Science and Department of Biology, Memorial University of Newfoundland. Special thanks to the contributors and collaborators who made this work possible.

---


## Contact

For questions or support, contact:

- Lourdes Peña-Castillo: [lourdes@mun.ca](mailto\:lourdes@mun.ca)

