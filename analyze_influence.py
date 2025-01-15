import json
import numpy as np
import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import kendalltau, spearmanr, pearsonr
from viral_centrality import viral_centrality  # Make sure this function is accessible

# Load data
with open('congress_network_data.json') as f:
    data = json.load(f)

# Extract data from JSON
inList = data[0]['inList']
inWeight = data[0]['inWeight']
outList = data[0]['outList']
outWeight = data[0]['outWeight']
usernameList = data[0]['usernameList']

# Create a directed graph
G = nx.DiGraph()
for i, username in enumerate(usernameList):
    G.add_node(i, username=username)

# Add edges with weights
for i, (out_nodes, weights) in enumerate(zip(outList, outWeight)):
    for j, weight in zip(out_nodes, weights):
        G.add_edge(i, j, weight=weight)

# Function to run ICM simulation
def run_icm_simulation(G, num_simulations=1000):
    spread_sizes = {node: 0 for node in G.nodes}
    for seed_node in G.nodes:
        total_activated = 0
        for _ in range(num_simulations):
            activated = {seed_node}
            newly_activated = {seed_node}
            while newly_activated:
                next_activated = set()
                for node in newly_activated:
                    for neighbor in G.successors(node):
                        if neighbor not in activated and np.random.rand() < G[node][neighbor]['weight']:
                            next_activated.add(neighbor)
                activated.update(next_activated)
                newly_activated = next_activated
            total_activated += len(activated)
        spread_sizes[seed_node] = total_activated / num_simulations
    return spread_sizes

# Monte Carlo ground truth
num_simulations = 1000  # Reduced to 1000 for debugging
avg_spread = run_icm_simulation(G, num_simulations)

# Calculate other centralities
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
closeness_centrality = nx.closeness_centrality(G, distance='weight')
try:
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06, weight='weight')
except nx.PowerIterationFailedConvergence:
    eigenvector_centrality = {node: 0 for node in G.nodes}

# Compute viral centrality inline
tol = 0.001
viral_centrality_values = viral_centrality(inList, inWeight, outList, Niter=-1, tol=tol)

# Convert centrality measures and influence spread to DataFrame
df = pd.DataFrame({
    'Node': list(G.nodes),
    'Degree Centrality': [degree_centrality[node] for node in G.nodes],
    'Betweenness Centrality': [betweenness_centrality[node] for node in G.nodes],
    'Closeness Centrality': [closeness_centrality[node] for node in G.nodes],
    'Eigenvector Centrality': [eigenvector_centrality[node] for node in G.nodes],
    'Viral Centrality': viral_centrality_values,
    'Influence Spread': [avg_spread[node] for node in G.nodes]
})

# Calculate correlations
correlations = {
    'Degree Centrality': pearsonr(df['Degree Centrality'], df['Influence Spread']),
    'Betweenness Centrality': pearsonr(df['Betweenness Centrality'], df['Influence Spread']),
    'Closeness Centrality': pearsonr(df['Closeness Centrality'], df['Influence Spread']),
    'Eigenvector Centrality': pearsonr(df['Eigenvector Centrality'], df['Influence Spread']),
    'Viral Centrality': pearsonr(df['Viral Centrality'], df['Influence Spread'])
}

# Print correlation results
for name, (corr, p_value) in correlations.items():
    print(f"Pearson correlation between {name} and Influence Spread: {corr:.3f}")
    print(f"P-value: {p_value:.3g}")

# Visualize the relationship using scatter plots
fig, axes = plt.subplots(3, 2, figsize=(15, 15))
axes = axes.flatten()

for i, (name, _) in enumerate(correlations.items()):
    axes[i].scatter(df[name], df['Influence Spread'])
    axes[i].set_title(f'{name} vs Influence Spread')
    axes[i].set_xlabel(name)
    axes[i].set_ylabel('Influence Spread')

plt.tight_layout()
plt.savefig('centrality_vs_influence_spread.pdf')

# Save the DataFrame as a table in a PDF
fig, ax = plt.subplots(figsize=(10, 6))  # Set the size of the figure
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)  # Adjust the scale of the table

plt.savefig('centrality_kendall_tau_results.pdf', bbox_inches='tight')




