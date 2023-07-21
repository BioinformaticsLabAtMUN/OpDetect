import sys
import re

def parse_gff3(file_path):
    gene_data = []
    genome_name = ""
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            if line.startswith('#'):
                if line.startswith('##sequence-region'):
                    genome_name = line.split()[1]
                continue
            fields = line.split('\t')
            if len(fields) < 9:
                continue
            if fields[2] == 'gene':
                gene_id_match = re.search(r'ID=([^;]+)', fields[8])
                gene_name_match = re.search(r'gene=([^;]+)', fields[8])
                if gene_id_match and gene_name_match:
                    gene_id = gene_id_match.group(1)
                    gene_name = gene_name_match.group(1)
                    start = int(fields[3])
                    end = int(fields[4])
                    strand = fields[6]
                    gene_data.append((gene_id, gene_name, start, end, strand))
    return genome_name, gene_data

def write_rnt_file(file_path, genome_name, gene_data):
    with open(file_path, 'w') as file:
        file.write(f"{genome_name} - 1..3805874\n")
        file.write(f"{len(gene_data)} RNAs\n")
        file.write("Location\tStrand\tLength\tPID\tGene\tSynonym\tCode\tCOG\tProduct\n")
        for i, data in enumerate(gene_data, start=1):
            gene_id, gene_name, start, end, strand = data
            file.write(f"{start}..{end}\t{strand}\t{end - start + 1}\t-\t{gene_name}\tEAM_{i:03d}\t-\t-\t-\n")

def write_ptt_file(file_path, genome_name, gene_data):
    with open(file_path, 'w') as file:
        file.write(f"{genome_name} - 1..3805874\n")
        file.write(f"{len(gene_data)} proteins\n")
        file.write("Location\tStrand\tLength\tPID\tGene\tSynonym\tCode\tCOG\tProduct\n")
        for i, data in enumerate(gene_data, start=1):
            gene_id, gene_name, start, end, strand = data
            file.write(f"{start}..{end}\t{strand}\t{end - start + 1}\t-\t{gene_name}\tEAM_{i:04d}\t-\t-\t-\n")

# Specify the input GFF3 file and output file prefix
gff3_file = sys.argv[1]
output_prefix = sys.argv[2]
rnt_file = output_prefix + '.rnt'
ptt_file = output_prefix + '.ptt'


genome_name, gene_data = parse_gff3(gff3_file)
write_rnt_file(rnt_file, genome_name, gene_data)
write_ptt_file(ptt_file, genome_name, gene_data)

# Run the script
# python 7_convert_gff3.py ../../operons/odb_data/txid224308/txid224308.gff3 ../../operons/odb_data/txid224308/txid224308/txid224308