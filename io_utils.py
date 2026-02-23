"""
Phylo Tree Builder: io_utils.py

"""

from pathlib import Path
from datetime import datetime

from Bio import SeqIO

import config

def read_fasta(in_folder: Path, out_file: Path, seq_type: str="fasta") -> Path:
    """Combine multiple FASTA files into one and standardise record IDs."""

    if not in_folder.exists():
        print(f"ERROR: Folder {in_folder} does not exist!")
        print("Please create the 'data' folder and add your FASTA files.")
        return None

    fasta_files = [i for i in in_folder.iterdir() if str(i.suffix).lower() == ".fasta"]
    if not fasta_files:
        print(f"ERROR: No FASTA files found in {in_folder}")
        print("Please add .fasta files to the data folder.")
        return None
    
    combined_records = []
    for file in fasta_files:
        try:
            records = list(SeqIO.parse(file, seq_type))
            if not records:
                print(f"Warning: {file.name} appears empty or invalid, skipping...")
                continue

            for idx, record in enumerate(records, start=1):
                # Check for empty sequences
                if len(record.seq) == 0:
                    print(f"Warning: Empty sequence found in {file.name}, skipping...")
                    continue

                base_id = file.stem 

                if idx > 1:
                    new_id = f"{base_id}_{idx}"
                else:
                    new_id = base_id

                record.id = new_id
                record.description = ""
                record.seq = record.seq.upper()
                combined_records.append(record)

        except Exception as e:
            print(f"Warning: Could not read {file.name}: {e}")
            print("Skipping this file...")
            continue

    if not combined_records:
        print("ERROR: No valid sequences found in any files!")
        return None

    SeqIO.write(combined_records, out_file, seq_type)

    print(f"✓ Combined FASTA written to: {out_file}")
    print(f"✓ Total sequences combined: {len(combined_records)}")
    
    return Path(out_file)

def generate_timestamp() -> str:

    timestamp = datetime.now().strftime(config.TIMESTAMP_FORMAT)

    return timestamp