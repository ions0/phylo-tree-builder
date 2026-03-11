"""
Phylo Tree Builder: config.py

"""
from pathlib import Path
import shutil
import yaml

# Paths
SCRIPT_PATH = Path(__file__).resolve().parent

# Defults
MUSCLE_PATH = shutil.which("muscle") or r"/usr/local/bin"
RESULTS_PATH = SCRIPT_PATH / "results"
FASTA_PATH = SCRIPT_PATH / "data"

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

# Override with config.yaml if present
config_file = SCRIPT_PATH / "config.yaml"
if config_file.exists():
    with open(config_file) as f:
        cfg = yaml.safe_load(f)

    FASTA_PATH = Path(cfg.get("paths", {}).get("fasta", FASTA_PATH))
    RESULTS_PATH = Path(cfg.get("paths", {}).get("results", RESULTS_PATH))
    DEFAULT_TREE_METHOD = cfg.get("tree", {}).get("default_method", DEFAULT_TREE_METHOD)
    DEFAULT_DISTANCE_METHOD = cfg.get("tree", {}).get("distance_method", DEFAULT_DISTANCE_METHOD)
    FIGURE_SIZE = tuple(cfg.get("visualisation", {}).get("figure_size", FIGURE_SIZE))
    DPI = cfg.get("visualisation", {}).get("dpi", DPI)
    DEFAULT_CLADE_COLOR = cfg.get("visualisation", {}).get("default_clade_color", DEFAULT_CLADE_COLOR)
    NCBI_EMAIL = cfg.get("ncbi", {}).get("email", None)
    NCBI_API_KEY = cfg.get("ncbi", {}).get("api_key", None)
    NCBI_FETCH_LIMIT = cfg.get("ncbi", {}).get("default_fetch_limit", 10)

def setup_directories(out_path: Path) -> None:
    """Create all required directories"""
    
    directories = [ 
        Path(out_path / "alignments"),
        Path(out_path / "trees")
    ]
    
    for directory in directories:
        try:
            directory.mkdir(parents=True, exist_ok=True)
        except OSError as e:
            raise RuntimeError(f"Failed to create directory: {directory}") from e
    
    print("Output directories initialised")