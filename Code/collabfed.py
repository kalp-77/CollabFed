import matplotlib.pyplot as plt
import matplotlib.animation as animation
import os

# Create results directory if it doesn't exist
os.makedirs("./results", exist_ok=True)

# Setup figure for BLS Multi-signature Collection animation
fig, ax = plt.subplots(figsize=(8, 5))

# Sample data for BLS multi-signature collection
nodes = ["CM1", "CM2", "CM3", "CM4", "CM5"]
signatures_collected = []

# Tree structure (M-ary): Simulate collection with binary (M=2)
tree_edges = {
    "CM1": ["CM2", "CM3"],
    "CM2": ["CM4", "CM5"]
}

def draw_tree(current_node, collected_nodes):
    """Recursive tree drawing with signature state"""
    children = tree_edges.get(current_node, [])
    for child in children:
        ax.plot([nodes.index(current_node), nodes.index(child)],
                [1, 0], color='gray', linestyle='-', linewidth=1)
        draw_tree(child, collected_nodes)
    
    color = 'green' if current_node in collected_nodes else 'lightgray'
    ax.scatter(nodes.index(current_node), 1 if current_node == "CM1" else 0, 
               color=color, s=500, edgecolor='black', zorder=5)
    ax.text(nodes.index(current_node), 1.1 if current_node == "CM1" else -0.1,
            current_node, ha='center', va='center', fontsize=9)

# Rewriting the BLS animation to include node labels below the nodes
def update_signature_collection_with_labels(frame):
    ax.clear()
    if frame < len(nodes):
        signatures_collected.append(nodes[frame])
    
    # Draw tree connections and nodes with labels below
    def draw_tree_with_labels(current_node, collected_nodes):
        children = tree_edges.get(current_node, [])
        for child in children:
            ax.plot([nodes.index(current_node), nodes.index(child)],
                    [1, 0], color='gray', linestyle='-', linewidth=1)
            draw_tree_with_labels(child, collected_nodes)
        
        color = 'green' if current_node in collected_nodes else 'lightgray'
        x = nodes.index(current_node)
        y = 1 if current_node == "CM1" else 0
        ax.scatter(x, y, color=color, s=500, edgecolor='black', zorder=5)
        ax.text(x, y - 0.15, current_node, ha='center', va='top', fontsize=9)

    draw_tree_with_labels("CM1", signatures_collected)
    ax.set_xlim(-1, len(nodes))
    ax.set_ylim(-1, 2)
    ax.set_title(f"BLS Multi-signature Collection\nCollected: {', '.join(signatures_collected)}", fontsize=10)
    ax.axis('off')

# Recreate and save the updated animation
fig, ax = plt.subplots(figsize=(8, 5))
signatures_collected = []  # Reset
ani_bls_labeled = animation.FuncAnimation(fig, update_signature_collection_with_labels, frames=len(nodes), interval=1000, repeat=False)
bls_gif_path = "./results/bls_multisig_collection.gif"
ani_bls_labeled.save(bls_gif_path, writer="pillow")

bls_gif_path
