"""
Phylo Tree Builder: validation.py

"""

from pathlib import Path
import config

from Bio import AlignIO

def muscle_path_check():

    if not Path(config.MUSCLE_PATH).exists():
        print("=" * 60)
        print("ERROR: MUSCLE alignment tool not found!")
        print(f"Expected location: {config.MUSCLE_PATH}")
        print("\nPlease either:")
        print("1. Install MUSCLE and add it to your PATH, or")
        print("2. Update MUSCLE_PATH in the script to point to muscle.exe")
        print("=" * 60)
        raise SystemExit("MUSCLE not found")

    print("✓ MUSCLE found at:", config.MUSCLE_PATH)   

def combine_and_align(combined_file, aligned_file):

    if combined_file is None:
        print("Stopping due to errors in reading FASTA files.")
        return

    if not aligned_file:
        print("Stopping due to alignment failure.")
        return

    alignment = AlignIO.read(aligned_file, "fasta")
    
    print(f"✓ Alignment loaded: {len(alignment)} sequences")
    print(f"✓ Alignment length: {alignment.get_alignment_length()}")

    if len(alignment) < 3:
        print("WARNING: Only", len(alignment), "sequences found.")
        print("You need at least 3 sequences to build a meaningful tree.")
        response = input("Continue anyway? (y/n): ")
        if response.lower() != "y":
            return

    return alignment
