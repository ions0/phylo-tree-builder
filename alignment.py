"""
Phylo Tree Builder: alignment.py

"""

import subprocess
from pathlib import Path

def align_fasta(in_file: Path, out_file: Path, muscle_path: str) -> Path:
    """Run MUSCLE alignment on the input FASTA and save aligned output."""
    
    if not in_file.exists():
        print(f"ERROR: Input file {in_file} does not exist!")
        return None

    print(f"Running MUSCLE alignment (this may take a minute)...")

    try:
        result = subprocess.run(
            [muscle_path, "-in", str(in_file), "-out", str(out_file)],
            check=True, capture_output=True, text=True)
        
        if not out_file.exists():
            print("ERROR: MUSCLE did not create output file")
            return None
        if out_file.stat().st_size == 0:
            print("ERROR: MUSCLE created empty alignment file")
            return None

        print("✓ Alignment completed successfully:", out_file)
        return out_file

    except subprocess.CalledProcessError as e:
        print("=" * 60)
        print("ERROR: MUSCLE alignment failed!")
        print(f"Exit code: {e.returncode}")
        if e.stderr:
            print(f"Error message: {e.stderr}")
        print("=" * 60)
        return None

    except FileNotFoundError:
        print(f"ERROR: Could not run MUSCLE at {muscle_path}")
        return None