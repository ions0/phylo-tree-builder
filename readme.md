# Phylogenetic Tree Builder

A Python-based pipeline for constructing and visualising phylogenetic trees from fungal ITS (Internal Transcribed Spacer) sequences.

## Overview

This tool combines multiple FASTA files, performs multiple sequence alignment using MUSCLE, calculates genetic distances, and constructs a phylogenetic tree using distance-based methods with automated genus-based color coding.

## Features

- Combines multiple FASTA files into a single alignment
- Performs multiple sequence alignment with MUSCLE
- Constructs phylogenetic trees (Neighbor-Joining or UPGMA)
- Automatically color-codes taxa by genus
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
```

Install with: `pip install -r requirements.txt`

## Installation

1. Clone this repository
2. Install Python dependencies: `pip install -r requirements.txt`
3. Install MUSCLE:
   - Download from https://www.drive5.com/muscle/
   - Add to system PATH or update `MUSCLE_PATH` in `config.py`

## Usage

1. Place FASTA files in the `data/` folder (created automatically on first run)
2. Run: `python phylo_tree_builder.py`
3. Results will be saved in organised subfolders within `results/`:
   - `alignments/` - Combined and aligned FASTA files
   - `trees/` - Tree visualisations (PNG) and structure files (Newick)

## Input Format

- FASTA files with `.fasta` extension
- Each file should contain ITS sequences from a single species
- Sequences will be automatically labeled by filename
- File naming convention: `Genus_species.fasta` (e.g., `Agaricus_bisporus.fasta`)

## Configuration

Edit `config.py` to adjust paths and pipeline settings:

```python
# Paths
FASTA_PATH = SCRIPT_PATH / "data"
RESULTS_PATH = SCRIPT_PATH / "results"
ALIGNMENTS_PATH = RESULTS_PATH / "alignments"
TREES_PATH = RESULTS_PATH / "trees"

# Tree Construction
DEFAULT_DISTANCE_METHOD = "identity"
DEFAULT_TREE_METHOD = "nj"           # "nj" (Neighbor-Joining) or "upgma"

# Visualisation
FIGURE_SIZE = (14, 8)
DPI = 300
DEFAULT_CLADE_COLOR = "gray"
```

## Output

Files are timestamped to prevent overwrites:

**Alignments folder** (`results/alignments/`):
- `combined_YYYY_MM_DD_HHMMSS.fasta`: All input sequences combined
- `combined_aligned_YYYY_MM_DD_HHMMSS.fasta`: Multiple sequence alignment

**Trees folder** (`results/trees/`):
- `fungal_tree_YYYY_MM_DD_HHMMSS.png`: Tree visualisation (300 DPI)
- `fungal_tree_YYYY_MM_DD_HHMMSS.nwk`: Newick format tree structure

## Error Handling

The pipeline includes validation at each stage:
- Checks for MUSCLE installation before processing — exits cleanly if not found
- Validates FASTA file format and content
- Skips empty or corrupted sequence files with warnings
- Prompts user to confirm if fewer than 3 sequences are found
- Validates alignment output before tree construction

## Example Data

Sample ITS sequences from medicinal fungal genera:

- *Trametes* spp.
- *Ganoderma* spp.
- *Lentinula* spp.
- *Hericium* spp.
- *Cordyceps* spp.
- *Grifola* spp.

Sequences can be obtained from NCBI GenBank using ITS1/ITS2 region searches.

## Methods

- **Alignment**: MUSCLE v5.3 (Edgar, 2022)
- **Distance calculation**: Identity-based distance matrix
- **Tree construction**: Neighbor-Joining (Saitou & Nei, 1987)
- **Visualisation**: Biopython Phylo module with matplotlib
- **Color palette**: Seaborn HUSL palette (auto-generated per genus)

## Project Structure

```
phylo_tree_builder/
├── phylo_tree_builder.py    # Entry point — pipeline orchestration
├── config.py                # Paths, settings, directory setup
├── io_utils.py              # FASTA reading, combining, timestamp generation
├── alignment.py             # MUSCLE alignment wrapper
├── tree_construction.py     # Distance matrix, tree building, genus extraction
├── validation.py            # MUSCLE path check, alignment validation
├── visualisation.py         # Tree plotting, clade colouring, palette generation
├── requirements.txt         # Python dependencies
├── README.md                # This file
├── data/                    # Input FASTA files (auto-created)
└── results/                 # Output directory (auto-created)
    ├── alignments/          # Combined and aligned sequences
    └── trees/               # Visualisations and Newick files
```

## Learning Notes

This project was developed as a learning exercise in phylogenetic analysis and bioinformatics pipeline development. Key concepts demonstrated:

- Modular program structure without OOP
- File I/O and data validation in Python
- Integration with external bioinformatics tools (MUSCLE)
- Use of Biopython for sequence analysis
- Phylogenetic tree construction algorithms
- Data visualisation with matplotlib/seaborn
- Error handling and user experience design

## Version History

- **v1.0.1** (February 23, 2026): Refactored into modular structure; separated concerns across dedicated modules; fixed directory setup side effects; improved pipeline flow
- **v1.0.0** (November 20, 2025): Initial release

## Future Improvements

- [ ] Command-line argument support (argparse)
- [ ] Bootstrap analysis for branch support values
- [ ] Additional distance calculation methods (Jukes-Cantor, Kimura)
- [ ] Support for protein sequences
- [ ] Maximum likelihood tree construction
- [ ] Automated sequence download from NCBI
- [ ] Configuration file support (YAML/TOML)
- [ ] Tree rooting options
- [ ] Interactive tree visualisation

## Troubleshooting

**MUSCLE not found**: Ensure MUSCLE is installed and either in system PATH or update `MUSCLE_PATH` in `config.py`.

**No FASTA files found**: Place `.fasta` files in the `data/` folder with the correct extension.

**Alignment fails**: Check that sequences are valid DNA/RNA and from the same genetic region (e.g., all ITS sequences).

**Tree looks incorrect**: Ensure sequences are from homologous regions. Try switching `DEFAULT_TREE_METHOD` between `"nj"` and `"upgma"` in `config.py`.

## Author

Jared Cambridge - 2025

## Acknowledgments

Developed as part of a beginner bioinformatics learning project exploring phylogenetic analysis of medicinal fungi.
