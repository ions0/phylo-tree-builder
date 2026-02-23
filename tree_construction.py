"""
Phylo Tree Builder: tree_construction.py

"""
from Bio.Phylo.TreeConstruction import DistanceCalculator, DistanceTreeConstructor

import config

def get_genera(tree) -> list:

    """Extract unique genus names from tree terminal nodes.
    Parses terminal node names assuming format 'Genus_species' and 
    returns a list of unique genus names in lowercase."""

    genera = set()
    all_terminals = tree.get_terminals()

    for node in all_terminals:
        if node.name:
            genus_name = node.name.split("_")[0].lower()
            genera.add(genus_name)

    return list(genera)

def build_tree(alignment):

    calculator = DistanceCalculator("identity")
    dm = calculator.get_distance(alignment)
    constructor = DistanceTreeConstructor()
    
    if config.DEFAULT_TREE_METHOD == "nj":
        tree = constructor.nj(dm)
    elif config.DEFAULT_TREE_METHOD == "upgma":
        tree = constructor.upgma(dm)
    else:
        raise ValueError(f"Unknown tree method: {config.DEFAULT_TREE_METHOD}")
    print(f"✓ Phylogenetic tree constructed using: {config.DEFAULT_TREE_METHOD.upper()}")

    # Draw the tree without branch labels
    for node in tree.get_nonterminals():
        node.confidence = None
        node.name = None

    return tree