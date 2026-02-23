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
from alignment import align_fasta
from visualisation import generate_palette, plot_phylo_tree, get_genus_colors
from io_utils import read_fasta, generate_timestamp
from tree_construction import get_genera, build_tree
from validation import muscle_path_check, combine_and_align


def main():
    """
    Main workflow: reads FASTA files, performs multiple sequence alignment,
    constructs phylogenetic tree, and generates visualisation.

    Steps:
    1. Read and combine FASTA files from data/ folder
    2. Align sequences using MUSCLE
    3. Calculate distance matrix
    4. Construct phylogenetic tree (Neighbor-Joining)
    5. Visualise and save results

    """

    config.setup_directories()
    muscle_path_check()
    timestamp = generate_timestamp()

    combined_file = read_fasta(
    Path(config.FASTA_PATH), config.ALIGNMENTS_PATH / f"combined_{timestamp}.fasta")

    aligned_file = align_fasta(
        combined_file, config.ALIGNMENTS_PATH / f"combined_aligned_{timestamp}.fasta", config.MUSCLE_PATH)

    alignment = combine_and_align(combined_file, aligned_file)
    tree = build_tree(alignment)
    genus_colors = get_genus_colors(tree)
    n_species = len(tree.get_terminals())

    plot_phylo_tree(tree, genus_colors, n_species, timestamp, config.AXES_COL, config.BACK_COL)

if __name__ == "__main__":
    main()