"""
Phylo Tree Builder: phylo_tree_builder.py 
Author: Jared Cambridge
Date Started: November 20, 2025
Major Completion: November 26, 2025

Updated: February 24, 2026

Description:     
    Automated phylogenetic tree construction from FASTA sequences.
    Performs multiple sequence alignment using MUSCLE and constructs
    distance-based phylogenetic trees with colour-coded visualisation.

Version: 1.0.1
"""

from pathlib import Path

import config
from cli import parse_arguments, validate_arguments
from alignment import align_fasta
from visualisation import generate_palette, plot_phylo_tree, get_genus_colors
from io_utils import read_fasta, generate_timestamp
from tree_construction import get_genera, build_tree
from validation import muscle_path_check, combine_and_align
from ncbi_fetch import fetch_by_accession, fetch_by_term

def main():
    """
    Main workflow: reads FASTA files, performs multiple sequence alignment,
    constructs phylogenetic tree, and generates visualisation.

    Steps:
    1. Read and combine FASTA files from data/ folder, --input argument or NCBI fetching
    2. Align sequences using MUSCLE
    3. Calculate distance matrix
    4. Construct phylogenetic tree
    5. Visualise and save results

    """

    args = parse_arguments()
    timestamp = generate_timestamp()
    run_path = Path(args.output) / f"results_{timestamp}"
    validate_arguments(args)
    config.setup_directories(run_path)
    muscle_path_check()

    if args.fetch:
        fetch_outpath = config.FASTA_PATH / f"{args.fetch}_{timestamp}"
        fetch_outpath.mkdir(parents=True, exist_ok=True)
        fetch_by_term(args.fetch, fetch_outpath, limit=args.fetch_limit)

        combined_file = read_fasta(
            Path(fetch_outpath), Path(run_path) / "alignments" / f"combined_{timestamp}.fasta")

    elif args.accessions:
        accession_outpath = config.FASTA_PATH / f"accessions_{timestamp}"
        accession_outpath.mkdir(parents=True, exist_ok=True)
        fetch_by_accession(args.accessions, accession_outpath)
    
        combined_file = read_fasta(
            Path(accession_outpath), Path(run_path) / "alignments" / f"combined_{timestamp}.fasta")

    else:
        combined_file = read_fasta(
            Path(config.FASTA_PATH), Path(run_path) / "alignments" / f"combined_{timestamp}.fasta")

    aligned_file = align_fasta(
        combined_file, Path(run_path) / "alignments" / f"combined_aligned_{timestamp}.fasta", config.MUSCLE_PATH)

    alignment = combine_and_align(combined_file, aligned_file)
    tree = build_tree(alignment, args.method)
    genus_colors = get_genus_colors(tree)
    n_species = len(tree.get_terminals())

    plot_phylo_tree(tree, genus_colors, n_species, timestamp, config.AXES_COL, config.BACK_COL, run_path)

if __name__ == "__main__":
    main()