"""
Phylo Tree Builder: cli.py

"""

import argparse
from pathlib import Path

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

    parser.add_argument(
        "--fetch",
        type=str,
        help="Search term to fetch sequences from NCBI"
    )

    parser.add_argument(
        "--accessions",
        nargs="+",
        help="NCBI accession numbers to fetch",
    )

    parser.add_argument(
        "--fetch-limit",
        type=int,
        default=10,
        help="Max sequences to fetch (default: 10)"
    )

    return parser.parse_args()

def validate_arguments(args: argparse.Namespace) -> None:
    
    if not args.fetch and not args.accessions:
        if not Path(args.input).exists():
            raise SystemExit("ERROR: Input path does not exist")

        if not Path(args.output).exists() or not Path(args.output).is_dir():
            Path(args.output).mkdir(parents=True, exist_ok=True)