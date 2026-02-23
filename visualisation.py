"""
Phylo Tree Builder: visualisation.py

"""

import matplotlib.pyplot as plt
import matplotlib.colors
import seaborn as sns

from matplotlib.patches import Patch
from Bio import Phylo
from Bio.Phylo.BaseTree import Tree

import config
from tree_construction import get_genera

def plot_phylo_tree(
    tree: Tree, 
    genus_colors: dict, 
    n_species: int, 
    timestamp: str, 
    axes_col: str, 
    back_col: str
) -> None:

    """Visualise and save the phylogenetic tree with color-coded genera."""

    color_clades(tree, genus_colors)
    sns.set_theme(context="talk", style="white", font_scale=1.0)

    for clade in tree.get_terminals():
        if clade.name:
            parts = clade.name.split("_")
            clade.name = f"{parts[0].capitalize()} {parts[1]}"

    fig = plt.figure(figsize=config.FIGURE_SIZE)
    ax = fig.add_subplot(1, 1, 1)
    ax.set_facecolor(axes_col)
    fig.patch.set_facecolor(back_col)
    legend_elements = [Patch(facecolor=color, label=genus.capitalize())
                        for genus, color in genus_colors.items()] 
                        
    ax.legend(handles=legend_elements, loc="upper left", bbox_to_anchor=(1.02, 1.0), 
                                                            title="Genera", fontsize=14)

    ax.set_xlabel("Genetic Distance", fontsize=12)
    ax.set_title(f"Phylogenetic Relationships of Medicinal Fungi Based on (n={n_species}) ITS Sequences")
    ax.set_ylabel("Taxa", fontsize=12)

    Phylo.draw(tree, axes=ax, do_show=False)
    Phylo.write(tree, config.TREES_PATH / f"fungal_tree_{timestamp}.nwk", "newick")

    plt.tight_layout()
    plt.savefig(config.TREES_PATH / f"fungal_tree_{timestamp}.png",dpi=config.DPI, bbox_inches="tight")
    plt.show()

def color_clades(tree: Tree, genus_colors: dict) -> None:
    """Assign colors to tree clades based on genus names."""

    for clade in tree.find_clades():
        matched = False
        if clade.name:
            for genus, color in genus_colors.items():
                if genus in clade.name.lower():
                    clade.color = color 
                    matched = True
                    break
        if not matched:
            clade.color = config.DEFAULT_CLADE_COLOR

def get_genus_colors(tree: Tree) -> dict:

    # Extract number of genera and assign colour
    genera = get_genera(tree)
    colors = generate_palette(len(genera))
    
    return dict(zip(genera, colors))

def generate_palette(n_genera: int) -> list:
    """Generate color palette for genus visualization."""

    colors = sns.color_palette("husl", n_colors=n_genera)
    hex_colors = [matplotlib.colors.rgb2hex(color) for color in colors]
    return hex_colors
