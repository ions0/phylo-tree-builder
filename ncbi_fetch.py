"""
Phylo Tree Builder: ncbi_fetch.py

"""

from pathlib import Path

from Bio import Entrez, SeqIO
from Bio.Seq import UndefinedSequenceError

from config import NCBI_API_KEY, NCBI_EMAIL

if not NCBI_EMAIL:
    raise ValueError("NCBI email not set - add your email to config.yaml under ncbi.email")

Entrez.email = NCBI_EMAIL
if NCBI_API_KEY:
    Entrez.api_key = NCBI_API_KEY

def fetch_by_accession(accessions: list[str], out_dir: Path) -> None:
    handle = Entrez.efetch(db="nucleotide", id=",".join(accessions), rettype="gb", retmode="text")
    _save_sequence(handle, out_dir)

def fetch_by_term(term: str, out_dir: Path, limit: int = 10) -> None:

    term_organism = f"{term}[organism]"

    handle = Entrez.esearch(db="nucleotide", term=term_organism, retmax=limit)
    
    ids = Entrez.read(handle)["IdList"]
    if not ids:
        raise ValueError(f"No sequences found for: {term}")

    handle = Entrez.efetch(db="nucleotide", id=",".join(ids), rettype="gb", retmode="text")
    _save_sequence(handle, out_dir)

def _save_sequence(handle, out_dir: Path) -> None:

    sequences = list(SeqIO.parse(handle, "gb"))
    for idx, seq in enumerate(sequences):
        
        genus = seq.annotations["taxonomy"][-1]
        organism_name = seq.annotations["organism"].replace(" ", "_")

        if str(organism_name).startswith(genus):
            seq.id = f"{organism_name}_{idx}"
        else:
            seq.id =  f"{genus}_{organism_name}_{idx}"

        try:
            out_path = out_dir / f"{seq.id}.fasta"
            SeqIO.write(seq, out_path, "fasta")

        except UndefinedSequenceError:
            print("Sequence content is undefined")
            continue
    
    print(f"{len(sequences)} sequences saved to {out_dir}")
