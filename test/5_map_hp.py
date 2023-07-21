import pandas as pd
import sys

txid = sys.argv[1]
DIR = '../../operons/data_odb/'+txid+'/'

# prepare ncbi_gff
def merge_gff3(file_path):
    merged_data = {}
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if not line.startswith('#') and line != '':
                fields = line.split('\t')
                chromosome = fields[0]
                start = fields[3]
                end = fields[4]
                strand = fields[6]
                chromosome = fields[0]
                key = (chromosome, start, end, strand)
                if key in merged_data:
                    merged_data[key].extend(fields[8:])
                else:
                    merged_data[key] = fields[8:]

    merged_lines = []
    for key, values in merged_data.items():
        # merged_values = ';'.join(values)
        # merged_line = '\t'.join(list(key) + merged_values)

        # join the values with a semicolon, and then join them to key with a tab
        merged_line = '\t'.join(list(key) + [';'.join(values)])

        merged_line = 'Chromosome\tena\tgene\t' + merged_line.split('\t')[1] + '\t' + merged_line.split('\t')[2] + '\t.\t' + merged_line.split('\t')[3] + '\t.\t' + merged_line.split('\t')[4]

        merged_lines.append(merged_line)

    print(merged_lines[1])

    merged_file_path = '5_merged.gff3'
    with open(merged_file_path, 'w') as merged_file:
        merged_file.write('\n'.join(merged_lines))

    print(f"Merge completed. Merged data written to '{merged_file_path}'.")

NCBI_gff_file = DIR + 'ncbi_'+txid+'.gff3'
# merge_gff3(NCBI_gff_file)
# then do bedtools intersect -a ../../operons/data_odb/txid85962/gene_annotation.bed -b 5_merged.gff3 -wa -wb -f 0.9 > 5_map_hp.bed

def read_pred(file_path):
    preds = []
    with open(file_path, 'r') as file:
        
        genes = []
        for line in file:
            line = line.strip()
            if not line:
                continue
            elif line.startswith("Operon"):
                flag = True
                # join genes by ', 
                genes = ', '.join(genes)
                # if genes is not empty, add it to preds
                if genes:
                    preds.append(genes)

                genes = []
            else:
                genes.append(line.split('\t')[1])
        
    return pd.DataFrame(preds, columns=['Genes'])

pred_file = DIR + 'of_outputs/operons.tsv'
preds = read_pred(pred_file)

map_file = '5_map_hp.bed'
map = pd.read_csv(map_file, sep='\t', header=None)
map.columns = ['chromosome', '.', '.', 'start', 'end', '.', 'strand', '.', 'name', 'chromosome', '.', '.', 'start', 'end', '.', 'strand', '.', 'description']

# for each row, extract the genes and replace them
def find_name(row):
    genes = row['Genes'].split(', ')
    new_genes = []

    for gene in genes:
        name = map[map['description'].str.contains(gene, case=False)].name
        try:
            new_genes.append(name.values[0])
        except:
            pass

    row['new_Genes'] = ','.join(new_genes)
    return row

preds = preds.apply(find_name, axis=1)

# to list
preds = preds[['new_Genes']]

# remove empty rows
preds = preds[preds['new_Genes'] != '']

# save to file operons.txt
preds.to_csv(DIR + 'of_outputs/operons.txt', sep='\t', index=False, header=False)
