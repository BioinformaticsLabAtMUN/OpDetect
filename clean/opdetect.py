import os
import subprocess


# Step 1: Quality control using fastp for single-end/pair-end reads
def quality_control(fastq_file, fastq_file_2=None, args=None):
    output_report = f"report_{os.path.basename(fastq_file)}.html"

    # Prepare fastp command for single-end/pair-end reads
    cmd_parts = ["fastp", f"-i {fastq_file}"]
    if fastq_file_2:
        cmd_parts.extend([f"-I {fastq_file_2}", f"-O cleaned_{fastq_file_2}"])
    cmd_parts.extend([f"-o cleaned_{fastq_file}", f"-h {output_report}"])

    if args:
        for arg, value in args.items():
            cmd_parts.append(f"{arg} {value}")

    script = " ".join(cmd_parts)
    subprocess.run(script, shell=True)

# Step 2: Align fastq file to merged fasta files
def align(fastq_file, fasta_files, fastq_file_2=None):
    # Merge all fasta files into one
    merged_fasta_file = "merged.fasta"
    with open(merged_fasta_file, "w") as f:
        for fasta_file in fasta_files:
            with open(fasta_file, "r") as f2:
                f.write(f2.read())

    index_dir = "index"
    index_path = os.path.join(index_dir, "index")

    # Index merged fasta file
    if not os.path.exists(index_dir):
        os.mkdir(index_dir)
    subprocess.run(f"hisat2-build -p 16 {merged_fasta_file} {index_path} -q", shell=True)

    # Align fastq file to merged fasta file
    output_sam_file = f"aligned_{os.path.basename(fastq_file)}.sam"
    hisat_command = ["hisat2", "-p 8", f"-x {index_path}"]
    
    if fastq_file_2:
        hisat_command.extend(["-1", fastq_file, "-2", fastq_file_2])
    else:
        hisat_command.extend(["-U", fastq_file])
    
    hisat_command.extend(["-S", output_sam_file])
    
    subprocess.run(" ".join(hisat_command), shell=True)

    return output_sam_file

# Step 3: Process alignment results, extract read counts
def process_alignment_results(sam_file, output_file="read_counts"):

    # Convert SAM to BAM
    subprocess.run(f"samtools view -b -o {sam_file}.bam {sam_file}", shell=True)

    # Sort BAM
    subprocess.run(f"samtools sort {sam_file}.bam -o {sam_file}.sorted.bam", shell=True)

    # Index sorted BAM
    subprocess.run(f"samtools index {sam_file}.sorted.bam", shell=True)

    # Generate coverage BED file
    subprocess.run(f"bedtools genomecov -ibam {sam_file}.sorted.bam > {output_file}.bed", shell=True)

    return f"{output_file}.bed"


# Step 4: Feature extraction
def feature_extraction(bed_file, output_file="features"):
    # python integrate.py txid224308,txid196627,txid511145,txid85962,txid297246,txid169963,txid272634 ../../operons/data_odb gene_annotation.bed base_cov labels data_integrated.pkl
    # python process.py ../../operons/data_odb data_integrated.pkl data_processed
    # python visualize.py ../../operons/data_odb data_processed_vis.pkl

    pass

# Main function
def main():

    # Step 1: Quality control
    fastq_file = "test.fastq"
    
    # Define fastp arguments as a dictionary
    fastp_args = {
        "-5": "",
        "--cut_front_window_size": "1",
        "--cut_front_mean_quality": "3",
        "-r": "",
        "--cut_right_window_size": "4",
        "--cut_right_mean_quality": "15"
    }

    quality_control(fastq_file, args=fastp_args)

    # Step 2: Align fastq file to fasta files
    fastq_file = "test.fastq"
    fasta_files = ["test.fasta"]
    sam_file = align(fastq_file, fasta_files)

    # Step 3: Process alignment results
    bed_file = process_alignment_results(sam_file)

    # Step 4: Feature extraction
    gff3_file = "test.gff3"
    feature_extraction(bed_file, gff3_file)

if __name__ == "__main__":
    main()
 