import pandas as pd
import sys

txid = sys.argv[1]
DIR = '../../operons/data_odb/'+txid+'/'

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

        merged_lines.append(merged_line)


    merged_file_path = '5_merged.gff3'
    with open(merged_file_path, 'w') as merged_file:
        merged_file.write('\n'.join(merged_lines))

    print(f"Merge completed. Merged data written to '{merged_file_path}'.")

# Usage example
file_path = DIR + txid +'.gff3'  # Replace with your GFF3 file path
merge_gff3(file_path)

# ------------------------

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

# read files

# read merged file and put it in a df
gff_file = '5_merged.gff3'
gff = pd.read_csv(gff_file, sep='\t', header=None)
gff.columns = ['chromosome', 'start', 'end', 'strand', 'description']

# read our bed file and put it in a df
org_gff_file = DIR + 'gene_annotation.bed'  # Replace with your BED file path
org_gff = pd.read_csv(org_gff_file, sep='\t', header=None)
org_gff.columns = ['chromosome', '.', '.', 'start', 'end', '.', 'strand', '.', 'name']

preds_file = DIR + 'of_outputs/operons.tsv' 
preds = read_pred(preds_file)


# merge org_gff and gff with (chromosome, start, end, strand) as key 
map = pd.merge(org_gff, gff, on=['chromosome', 'start', 'end', 'strand'], how='inner')
# map = map[['name', 'description']]


# for each row, extract the genes and replace them
def find_name(row):
    genes = row['Genes'].split(', ')
    new_genes = []

    for gene in genes:
        if txid == 'txid224326':
            # replace 'bb' in gene to 'BB_'
            gene = gene.replace('bb', 'BB_')
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
