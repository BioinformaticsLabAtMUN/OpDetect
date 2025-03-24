# OpDetect: A convolutional and recurrent neural network classifier for precise and sensitive operon detection from RNA-seq data
## Abstract

An operon refers to a group of neighbouring genes belonging to one or more overlapping
transcription units that are transcribed in the same direction and have at least one gene
in common. Operons are a characteristic of prokaryotic genomes. Identifying which
genes belong to the same operon facilitates understanding gene function and regulation.
There are several computational approaches for operon detection; however, many of
these computational approaches have been developed for a specific target bacterium or
require information only available for a restricted number of bacterial species. Here, we
develop a novel general method, OpDetect, that directly utilizes RNA-sequencing
(RNA-seq) reads as a signal over nucleotide bases in the genome. This representation
enabled us to employ a convolutional and recurrent deep neural network architecture
which demonstrated superior performance in terms of recall, f1-score and AUROC
compared to previous approaches. Additionally, OpDetect showcases species-agnostic
capabilities, successfully detecting operons in a wide range of bacterial species and even
in  *Caenorhabditis elegans*, one of few eukaryotic organisms known to have operons.

---

## Key Features

- **Species-Agnostic**: Works across a wide range of bacterial species and can even detect operons in *Caenorhabditis elegans*, one of few eukaryotes known to have operons.
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

### Setup

1. Clone the repository:
   ```bash
   git clone https://github.com/BioinformaticsLabAtMUN/OpDetect.git
   cd OpDetect
   ```
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

---

## Usage

### Data Preparation

1. **Prepare Read Counts and Labels**:

   - The initial steps in processing the data involve trimming and filtering the raw sequencing data in FASTQ format. We performed this process using Fastp (version 0.23.1). The trimmed and filtered FastQ files are then aligned to the reference genomes using HISAT2 (version 2.2.1), and the read coverage for each genome base is extracted using SAMtools (version 1.17) and BEDtools (version 2.30.0). The specific commands for data preparation (excluding mapping) are:

     A) Fastp command:
     ```
       fastp -i in.R1.fq [-I in.R2.fq] -o out.R1.fq [-O out.R2.fq] 
       --cut_front_window_size 1 --cut_front_mean_quality 3 
       -r --cut_right_window_size 4 --cut_right_mean_quality 15
     ```
     
     B) Commands to convert SAM to BAM and sort BAM:
     ```
       samtools view -b -o BAM_file.bam SAM_file.sam
       samtools sort BAM_file.bam -o sorted_BAM_file.bam
     ```
     
     C) Bedtools command to obtain read counts:
     ```
       bedtools genomecov -d -ibam sorted_BAM_file.bam > read_counts.bed
     ```
     
   - Use the scripts in `2_process_reads` and `3_labels` directories to prepare the read count files and labels.

2. **Prepare Data Directory**:

   - Create a subdirectory in `0_data` named with the `txid` of the organism (e.g., `txid12345`).
   - Place the following files in the subdirectory:
     - Read count files with names like `base_cov_SAMPLEID`.
     - Gene annotation file (e.g., `gene_annotation.bed`).
     - [Optional] Labels file listing genes in the same operon on the same line. 

3. **Process Data and Run Test**:
   From the main directory, execute the following commands:

   ```bash
   python 4_data_process/integrate.py txid12345 0_data gene_annotation.bed base_cov labels 0_data/data_integrated.pkl
   ```

   - Replace `txid12345` with your organism-specific directory name.
   - Adjust paths to match your directory structure.

   ```bash
   python 4_data_process/process.py 0_data data_integrated.pkl data_processed.npz TEST 0_data/txid12345/gene_pairs.csv
   ```

   - Outputs `gene_pairs.csv` containing gene-pair labels.

4. **Run Test**:
   Go to the directory `6_test`, then run:

   ```bash
   python test.py ../0_data models/versions OpDetect data_processed.npz ../0_data/txid12345/gene_pairs.csv
   ```

### Example Workflow

Below is an example workflow with `txid272942`:

```bash
python 4_data_process/integrate.py txid272942 0_data gene_annotation.bed base_cov labels 0_data/data_integrated.pkl
python 4_data_process/process.py 0_data data_integrated.pkl data_processed.npz TEST 0_data/txid272942/gene_pairs.csv
cd 6_test/
python test.py ../0_data models/versions OpDetect data_processed.npz ../0_data/txid272942/gene_pairs.csv
```

The resulting predicted labels will be saved in `7_compare/outputs/OpDetect_txid272942.csv`.

Note: If the label file is unavailable and you only want predictions without true labels, enter NA in place of the label file name when running integrate.py. This will assign a value of -1 to every gene pair instead of the true labels. The code will then be modified as follows:
```bash
python 4_data_process/integrate.py txid272942 0_data gene_annotation.bed base_cov NA 0_data/data_integrated.pkl
python 4_data_process/process.py 0_data data_integrated.pkl data_processed.npz TEST 0_data/txid272942/gene_pairs.csv
cd 6_test/
python test.py ../0_data models/versions OpDetect data_processed.npz ../0_data/txid272942/gene_pairs.csv
```

### Example Test Output

```
Done with  txid272942
Size:  3652
Labels: 
label
0    2061
1    1426
2     165
Name: count, dtype: int64
--------------------------------------- 

resample done
scale done
smooth done
same_length done
combine done
Model: "functional"
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━┓
┃ Layer (type)                         ┃ Output Shape                ┃         Param # ┃
┡━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━┩
│ input_layer (InputLayer)             │ (None, 150, 6, 3)           │               0 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ conv2d (Conv2D)                      │ (None, 146, 1, 64)          │           5,824 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ lambda (Lambda)                      │ (None, 146, 64)             │               0 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ lstm (LSTM)                          │ [(None, 146, 64), (None,    │          33,024 │
│                                      │ 64), (None, 64)]            │                 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ self_attention (SelfAttention)       │ [(None, 1024), (None, 16,   │           2,560 │
│                                      │ 146)]                       │                 │
├──────────────────────────────────────┼─────────────────────────────┼─────────────────┤
│ dense (Dense)                        │ (None, 2)                   │           2,050 │
└──────────────────────────────────────┴─────────────────────────────┴─────────────────┘
 Total params: 43,458 (169.76 KB)
 Trainable params: 43,458 (169.76 KB)
 Non-trainable params: 0 (0.00 B)
********************txid272942********************
0 non-operons were not labeled and 0 operons were not labeled 

Classification report
              precision    recall  f1-score   support

           0       0.78      0.66      0.71      2061
           1       0.60      0.73      0.66      1426

    accuracy                           0.69      3487
   macro avg       0.69      0.69      0.69      3487
weighted avg       0.70      0.69      0.69      3487

Predicted   0.0   1.0   All
True                       
0          1357   704  2061
1           385  1041  1426
All        1742  1745  3487
Total F1 score and recall
F1 score: 0.6565752128666035
Recall: 0.7300140252454418
**************************************************
```

---

## Evaluation

### Metrics

- **Recall**
- **F1-score**
- **AUROC**

### Results

OpDetect consistently outperforms existing methods on validation organisms, achieving in 10-fold cross-validation:

- Recall: 88.94%
- F1-score: 89.50%
- AUROC: 0.89

---

## Citation

If you use OpDetect in your research, please cite:

Rezvan Karaji and Lourdes Peña-Castillo, "OpDetect: A Convolutional and Recurrent Neural Network Classifier for Precise and Sensitive Operon Detection from RNA-seq Data," *PLoS ONE*, 2024.

---

## Acknowledgments

This tool was developed at the Department of Computer Science and Department of Biology, Memorial University of Newfoundland. Special thanks to the contributors and collaborators who made this work possible.

---

## License

[MIT License](LICENSE)

---

## Contact

For questions or support, contact:

- Lourdes Peña-Castillo: [lourdes@mun.ca](mailto:lourdes@mun.ca)

