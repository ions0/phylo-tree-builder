"""
Phylo Tree Builder: cli.py

"""

import argparse

import config

def parse_arguments() -> argparse.Namespace:
    """
    Parse and validate command-line arguments.
    
    Returns:
        argparse.Namespace: Parsed arguments containing:
            - method: Joining method
            - input: Input directory path
            - output: Output directory path

    """

    parser = argparse.ArgumentParser(
        description="Phylo Tree Builder - Automated phylogenetic tree construction from FASTA sequences.",
        epilog="Example: python phylo_tree_builder --method nj --input /data/input-files --output /data/output-files"
    )

    parser.add_argument(
        "--method",
        type=str,
        required=False,
        default=config.DEFAULT_TREE_METHOD,
        choices=["nj", "upgma"],
        help="Select construction method for tree building (nj or upgma)"
    )

    parser.add_argument(
        "--input",
        type=str,
        required=False,
        default=config.FASTA_PATH,
        help="Select input files for trees"
    )

    parser.add_argument(
        "--output",
        type=str,
        required=False,
        default=config.RESULTS_PATH,
        help="Select output destination for trees"
    )

    return parser.parse_args()

def validate_arguments(args) -> None:
    pass