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


    merged_file_path = '3_merged.gff3'
    with open(merged_file_path, 'w') as merged_file:
        merged_file.write('\n'.join(merged_lines))

    print(f"Merge completed. Merged data written to '{merged_file_path}'.")

# Usage example
file_path = DIR + txid +'.gff3'  # Replace with your GFF3 file path
merge_gff3(file_path)

# ------------------------

# read files

# read merged file and put it in a df
gff_file = '3_merged.gff3'
gff = pd.read_csv(gff_file, sep='\t', header=None)
gff.columns = ['chromosome', 'start', 'end', 'strand', 'description']

# read our bed file and put it in a df
org_gff_file = DIR + 'gene_annotation.bed'  # Replace with your BED file path
org_gff = pd.read_csv(org_gff_file, sep='\t', header=None)
org_gff.columns = ['chromosome', '.', '.', 'start', 'end', '.', 'strand', '.', 'name']

preds_file = DIR + 'om_outputs/pairs.csv' 
preds = pd.read_csv(preds_file, sep='\t')
preds.columns = ['idGen1', 'idGen2', '.', '.', '.', '.', 'pred', '.']
preds = preds[['idGen1', 'idGen2', 'pred']]
# change pred column, Operon->1 and noOperon->0
preds['pred'] = preds['pred'].apply(lambda x: 1 if x == 'Operon' else 0)


# merge org_gff and gff with (chromosome, start, end, strand) as key 
map = pd.merge(org_gff, gff, on=['chromosome', 'start', 'end', 'strand'], how='inner')
map = map[['name', 'description']]


# print(map.head())

# for idGen1, idGen2 in preds, find each of them in the map['description'] and return the name in the map['name'] of the same row as name_1 or name_2
def find_name(id):
    # try:
    name = map[map['description'].str.contains(id, case=False)].name
    try:
        return name.values[0]
    except:
        return 
    # except:
    #     print(id)

preds['name_1'] = preds.apply(lambda x: find_name(x['idGen1']), axis=1)
preds['name_2'] = preds.apply(lambda x: find_name(x['idGen2']), axis=1)

# remove rows with nan values
preds = preds.dropna()

preds = preds[['name_1', 'name_2', 'pred']]

# save preds to csv
preds.to_csv(DIR + 'om_outputs/preds.csv', index=False)
