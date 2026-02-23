"""
Phylo Tree Builder: config.py

"""
from pathlib import Path
import shutil

# Paths
SCRIPT_PATH = Path(__file__).resolve().parent
MUSCLE_PATH = shutil.which("muscle") or r"/usr/local/bin"
RESULTS_PATH = SCRIPT_PATH / "results"
FASTA_PATH = SCRIPT_PATH / "data"
ALIGNMENTS_PATH = RESULTS_PATH / "alignments"
TREES_PATH = RESULTS_PATH / "trees"

# Tree Construction
DEFAULT_DISTANCE_METHOD = "identity"
DEFAULT_TREE_METHOD = "nj"

# Visualisation
FIGURE_SIZE = (14, 8)
DPI = 300
DEFAULT_CLADE_COLOR = "gray"
AXES_COL = "#ffffff"
BACK_COL = "#f2eee4"

TIMESTAMP_FORMAT = "%Y_%m_%d_%H%M%S"

def setup_directories() -> None:
    """Create all required directories"""
    
    directories = [
        FASTA_PATH,
        RESULTS_PATH,
        ALIGNMENTS_PATH,
        TREES_PATH
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create directory: {directory}") from e
    
    print("Output directories initialised")