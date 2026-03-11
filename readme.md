# Phylogenetic Tree Builder

A Python-based pipeline for constructing and visualising phylogenetic trees from nucleotide sequences, with support for local FASTA files and direct sequence retrieval from NCBI.

## Overview

This tool combines multiple FASTA files, performs multiple sequence alignment using MUSCLE, calculates genetic distances, and constructs a phylogenetic tree using distance-based methods with automated genus-based colour coding. Sequences can be sourced locally or fetched directly from NCBI GenBank by search term or accession number.

## Features

- Combines multiple FASTA files into a single alignment
- Performs multiple sequence alignment with MUSCLE
- Constructs phylogenetic trees (Neighbor-Joining or UPGMA)
- Automatically colour-codes taxa by genus
- Fetches sequences directly from NCBI by search term or accession number
- Extracts organism names and taxonomy from GenBank metadata
- Validates input files and alignment quality
- Generates high-resolution publication-ready figures
- Exports trees in Newick format

## Requirements

### Software
- Python 3.8+
- MUSCLE v5.x alignment tool

### Python Libraries
```
biopython>=1.84
matplotlib>=3.8.0
seaborn>=0.13.0
pyyaml>=6.0
```

Install with: `pip install -r requirements.txt`

## Installation

1. Clone this repository
2. Install Python dependencies: `pip install -r requirements.txt`
3. Install MUSCLE:
   - Download from https://www.drive5.com/muscle/
   - Add to system PATH or update `MUSCLE_PATH` in `config.py`
4. Add your NCBI email to `config.yaml` under `ncbi.email` (required for NCBI fetch)

## Usage

### Local FASTA files
1. Place FASTA files in the `data/` folder
2. Run: `python phylo_tree_builder.py`

### Fetch by search term
```
python phylo_tree_builder.py --fetch "Ganoderma lucidum" --fetch-limit 20
```

### Fetch by accession numbers
```
python phylo_tree_builder.py --accessions MK348425 MK348426 MK348427
```

Results are saved in timestamped subfolders within `results/`:
- `alignments/` - Combined and aligned FASTA files
- `trees/` - Tree visualisations (PNG) and Newick structure files

## Arguments

| Argument | Options | Default | Description |
|---|---|---|---|
| `--method` | `nj`, `upgma` | `nj` | Tree construction method |
| `--input` | any valid path | `data/` | Input directory containing local FASTA files |
| `--output` | any valid path | `results/` | Output directory for results |
| `--fetch` | search string | — | Search term to fetch sequences from NCBI |
| `--accessions` | accession numbers | — | One or more NCBI accession numbers to fetch |
| `--fetch-limit` | integer | `10` | Maximum number of sequences to fetch |

## Input Format

### Local files
- FASTA files with `.fasta` extension placed in the `data/` folder
- File naming convention: `Genus_species.fasta` (e.g., `Ganoderma_lucidum.fasta`)
- Multiple sequences per file are supported

### NCBI fetch
- Sequences are fetched in GenBank format and saved as individual FASTA files
- Organism names and taxonomy are extracted automatically from GenBank metadata
- Files are saved to a timestamped subdirectory within `data/` to avoid mixing with local files

## Configuration

Edit `config.yaml` to adjust settings without modifying Python code:
```yaml
paths:
  fasta: data/
  results: results/

tree:
  default_method: nj           # "nj" (Neighbor-Joining) or "upgma"
  distance_method: identity

visualisation:
  figure_size: [14, 8]
  dpi: 300
  default_clade_color: gray

ncbi:
  email: your@email.com        # Required for NCBI fetch
  api_key:                     # Optional — increases rate limits
  default_fetch_limit: 10
```

## Output

Results are saved in a timestamped folder to prevent overwrites:
```
<output>/
└── results_YYYY_MM_DD_HHMMSS/
    ├── alignments/
    │   ├── combined_YYYY_MM_DD_HHMMSS.fasta
    │   └── combined_aligned_YYYY_MM_DD_HHMMSS.fasta
    └── trees/
        ├── fungal_tree_YYYY_MM_DD_HHMMSS.png
        └── fungal_tree_YYYY_MM_DD_HHMMSS.nwk
```

When using `--fetch` or `--accessions`, downloaded sequences are also saved to a timestamped subdirectory within `data/` for reuse.

## Error Handling

The pipeline includes validation at each stage:
- Checks for MUSCLE installation before processing — exits cleanly if not found
- Validates FASTA file format and content
- Skips empty or corrupted sequence files with warnings
- Skips GenBank records with undefined sequence content
- Prompts user to confirm if fewer than 3 sequences are found
- Validates alignment output before tree construction
- Input path validation is skipped when using `--fetch` or `--accessions`

## Project Structure

```
phylo_tree_builder/
├── phylo_tree_builder.py       # Entry point — pipeline orchestration
├── config.py                   # Paths, settings, directory setup
├── config.yaml                 # User-facing configuration overrides
├── io_utils.py                 # FASTA reading, combining, timestamp generation
├── alignment.py                # MUSCLE alignment wrapper
├── tree_construction.py        # Distance matrix, tree building, genus extraction
├── validation.py               # MUSCLE path check, alignment validation
├── visualisation.py            # Tree plotting, clade colouring, palette generation
├── ncbi_fetch.py               # NCBI sequence retrieval via Entrez
├── cli.py                      # Argument parsing and validation
├── requirements.txt            # Python dependencies
├── README.md                   # This file
├── data/                       # Input FASTA files (auto-created)
│   └── <term>_YYYYMMDD/        # NCBI fetch output (auto-created per run)
└── results/
    └── results_YYYY_MM_DD_HHMMSS/
        ├── alignments/
        └── trees/
```

## Methods

- **Alignment**: MUSCLE v5.3 (Edgar, 2022)
- **Distance calculation**: Identity-based distance matrix
- **Tree construction**: Neighbor-Joining (Saitou & Nei, 1987) or UPGMA
- **Sequence retrieval**: NCBI Entrez E-utilities via Biopython
- **Visualisation**: Biopython Phylo module with matplotlib
- **Colour palette**: Seaborn HUSL palette (auto-generated per genus)

## Version History

- **v1.2.0** (March 11, 2026): Added NCBI sequence fetching (`--fetch`, `--accessions`); organism names and taxonomy extracted from GenBank metadata; isolated fetch output directories; fixed multi-word organism name handling in visualisation
- **v1.1.1** (March 9, 2026): Added `config.yaml` support for user-facing settings override
- **v1.1.0** (March 4, 2026): Added CLI argument support (`--method`, `--input`, `--output`)
- **v1.0.1** (February 23, 2026): Refactored into modular structure; separated concerns across dedicated modules
- **v1.0.0** (November 20, 2025): Initial release

## Future Improvements

- [x] Command-line argument support (argparse)
- [x] Configuration file support (YAML)
- [x] Automated sequence download from NCBI
- [ ] Bootstrap analysis for branch support values
- [ ] Additional distance calculation methods (Jukes-Cantor, Kimura)
- [ ] Support for protein sequences
- [ ] Maximum likelihood tree construction
- [ ] Tree rooting options
- [ ] Interactive tree visualisation

## Troubleshooting

**MUSCLE not found**: Ensure MUSCLE is installed and either in system PATH or update `MUSCLE_PATH` in `config.py`.

**No FASTA files found**: Place `.fasta` files in the `data/` folder with the correct extension.

**NCBI fetch returns no results**: Check your search term and ensure your email is set in `config.yaml`. Try narrowing the search or using accession numbers directly.

**Alignment fails**: Check that sequences are valid DNA/RNA and from the same genetic region.

**Tree looks incorrect**: Ensure sequences are from homologous regions. Try switching between `nj` and `upgma` methods.

## Author

Jared Cambridge - 2026

## Acknowledgments

Developed as a learning project in bioinformatics pipeline development and phylogenetic analysis.
