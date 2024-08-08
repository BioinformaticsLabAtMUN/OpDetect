import pandas as pd
import numpy as np
import sys
import os

# make the coverage sequence for each gene
def genes_coverage(coverage, start, end, reversed=False):
    if reversed:
        # reverse the coverage list for genes in backward strand
        return coverage.coverage[start:end].to_numpy().flatten()[::-1]
    else:      
        return coverage.coverage[start:end].to_numpy().flatten()

# pair up consecutive genes
def make_pair(df, reversed=False, names=None):
    # sort genes by chromosome and start position
    if reversed:
        df = df.sort_values(['Chromosome', 'start'], ascending=[False, False]).reset_index(drop=True)
    else:
        df = df.sort_values(['Chromosome', 'start']).reset_index(drop=True)

    # pair up consecutive genes with the same chromosome
    paired = pd.DataFrame(columns=names)
    for chrom in df['Chromosome'].unique():
        chrom_df = df[df['Chromosome'] == chrom].reset_index(drop=True)

        first = chrom_df.copy()
        second = chrom_df.apply(np.roll, shift=-1)
        chrom_paired = pd.concat([first, second], axis=1)

        chrom_paired.columns = names
        # chrom_paired = chrom_paired[:-1]  # drop last row with NaN values
        paired = pd.concat([paired, chrom_paired], ignore_index=True)

    return paired


# make intergenic coverage sequence for each pair of genes
# flag = between first and last gene
def intergenic(coverage, row, genome_length, reversed=False, flag=False):
    if reversed:
        start = row.end_2
        end = row.start_1
        if row.start_1 < row.start_2:
            flag = True
    else:
        start = row.end_1
        end = row.start_2
        if row.start_2 < row.start_1:
            flag = True

    length = end - start - 1

    # between first and last gene
    if flag:
        part_1 = coverage.coverage[start + 1:].to_numpy().reshape((genome_length - start - 1))
        part_2 = coverage.coverage[:end].to_numpy().reshape((end))
        if reversed:
            intergenic_coverage = np.concatenate([part_1, part_2])[::-1]
        else:    
            intergenic_coverage = np.concatenate([part_1, part_2])

    elif length > 0 :
        intergenic_coverage = genes_coverage(coverage, start+1, end, reversed=reversed)
        
    # pairs with intersection
    else:
        intergenic_coverage = np.zeros(1)
        
    row['gene_1'] = row.coverage_1
    row['intergenic'] = intergenic_coverage
    row['gene_2'] = row.coverage_2

    return row


# hyperparameters
ANNOTATION_COLUMNS = ['Chromosome', 'ena', 'gene', 'start', 'end','.1', 'strand', '.2', 'name']
COVERAGE_COLUMNS = ['Chromosome', 'base_number', 'coverage']
COVERAGE_INDEX = ['base_number']
MIN_LENGTH = 150
REP_NUMBER = 6

if __name__ == '__main__':

    organisms = sys.argv[1].split(',')
    data_dir = sys.argv[2]
    annotation_file_name = sys.argv[3]
    coverage_file_name = sys.argv[4]
    label_file_name = sys.argv[5]
    output_path = sys.argv[6]

    TEST = False
    if len(sys.argv) == 8:
        TEST = True

    trains = []

    # for each folder(organism) in data_dir
    for folder in organisms:
        if os.path.isdir(str(data_dir + '/' + folder)):
            annotation_path = data_dir + '/' + folder + '/' + annotation_file_name
            coverage_path = data_dir + '/' + folder + '/' + coverage_file_name
            label_path = data_dir + '/' + folder + '/' + label_file_name

            # read annotation file
            annotation = pd.read_csv(annotation_path, names=ANNOTATION_COLUMNS, sep='\t')

            # Separate the strands
            forward = annotation[annotation.strand == '+'].reset_index(drop=True)
            backward = annotation[annotation.strand == '-'].reset_index(drop=True)

            sequences = []
            reps = [filename.split("base_cov_")[1] for filename in os.listdir(data_dir + '/' + folder) if filename.startswith(coverage_file_name)]

            for rep in reps:
                coverage_path_rep = coverage_path +'_'+ str(rep)
                coverage = pd.read_csv(coverage_path_rep, names = COVERAGE_COLUMNS, sep='\t', index_col=COVERAGE_INDEX).reset_index(drop=True)

                genome_length = coverage.shape[0]

                rep_forward = forward.copy()
                rep_backward = backward.copy()

                # make the coverage sequence for each gene
                rep_forward['coverage'] = forward.apply(lambda row: genes_coverage(coverage, row.start, row.end), axis=1)
                rep_backward['coverage'] = backward.apply(lambda row: genes_coverage(coverage, row.start, row.end, reversed=True), axis=1)

                # pair up consecutive genes
                names = [col + '_1' for col in rep_forward.columns] + [col + '_2' for col in rep_forward.columns]
                rep_forward = make_pair(rep_forward, names=names)
                rep_backward = make_pair(rep_backward, reversed=True, names=names)

                # make intergenic coverage sequence for each pair of genes
                rep_forward = rep_forward.apply(lambda row: intergenic(coverage, row, genome_length), axis=1)
                rep_backward = rep_backward.apply(lambda row: intergenic(coverage, row, genome_length, reversed=True), axis=1)

                # merge forward and backward
                rep_features = pd.concat([rep_forward, rep_backward], axis=0).reset_index(drop=True)
                rep_features = rep_features[['name_1', 'name_2', 'gene_1', 'intergenic', 'gene_2']]

                rep_index = reps.index(rep)
                rep_features.columns = ['name_1', 'name_2', 'gene_1_{}'.format(rep_index), 'intergenic_{}'.format(rep_index), 'gene_2_{}'.format(rep_index)]
                
                sequences.append(rep_features)
                # now sequences is a list of dataframes of dim (n, 5), cols = name_1, name_2, gene_1, intergenic, gene_2

            # add empty sequences to make all sequences the same length
            if len(reps) < REP_NUMBER:
                for i in range(len(reps), REP_NUMBER):
                    temp = sequences[0].copy()
                    temp.columns = ['name_1', 'name_2', 'gene_1_{}'.format(i), 'intergenic_{}'.format(i), 'gene_2_{}'.format(i)]
                    sequences.append(temp)

            # merge all the sequences
            features = sequences[0]
            for i in range(1, REP_NUMBER):
                features = pd.merge(features, sequences[i], on=['name_1', 'name_2'], how='outer')

                # remove rows with gene_1 or gene_2 of length 0 (i.e. no coverage)
                features = features[features.apply(lambda row: len(row[f'gene_1_{i}']) > 0 and len(row[f'gene_2_{i}']) > 0, axis=1)]

            # remove rows with NaN
            features.dropna(inplace=True)

            # add label
            labels = pd.read_csv(label_path, sep='\t')
            # merge features and labels
            def make_label_pair(operon_pair_list, genes):
                if len(genes) > 1:
                    for gene_1 in genes:
                        for gene_2 in genes:
                            if not gene_1 == gene_2:
                                operon_pair_list.append([gene_1, gene_2])
                                operon_pair_list.append([gene_2, gene_1])


            operon_pair_list=[]
            labels.apply(lambda row: make_label_pair(operon_pair_list, row[0].split(',')), axis=1)

            features['label'] = features.apply(lambda row: 1 if [row.name_1.split(',')[0], row.name_2.split(',')[0]] in operon_pair_list else 0, axis=1)
            features.reset_index(drop=True, inplace=True)

            # separate all the gene names in labels file and put them in a list
            gene_names = []
            labels.apply(lambda row: gene_names.extend(row[0].split(',')), axis=1)
            gene_names = list(set(gene_names))
            # print("labeled genes: ", gene_names)

            # if a pair is labeled 0 and either of the genes are not in the gene_names list, label 2
            features['label'] = features.apply(lambda row: 2 if row.label == 0 and (row.name_1.split(',')[0] not in gene_names or row.name_2.split(',')[0] not in gene_names) else row.label, axis=1)


            trains.append(features)

            print("Done with ", folder)
            print("Size: ", features.shape[0])
            print("Labels: ")
            print(features.label.value_counts())
            print("---------------------------------------", '\n')

    
        # combine all trains
    data = pd.concat(trains, axis=0).reset_index(drop=True)
    if not TEST:
        print("Total Size: ", data.shape[0])
        print("Total Labels: ")
        print(data.label.value_counts())

    # save data
    data.to_pickle(output_path)


