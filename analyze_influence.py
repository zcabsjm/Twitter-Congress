import json
import numpy as np
import networkx as nx
from matplotlib import pyplot as plt
from scipy.stats import pearsonr
from viral_centrality import viral_centrality

# Load data
with open('congress_network_data.json') as f:
    data = json.load(f)

inList = data[0]['inList']
inWeight = data[0]['inWeight']
outList = data[0]['outList']
outWeight = data[0]['outWeight']
usernameList = data[0]['usernameList']

# Create a directed graph
G = nx.DiGraph()

# Add nodes
for i, username in enumerate(usernameList):
    G.add_node(i, username=username)

# Add edges with weights
for i, (out_nodes, weights) in enumerate(zip(outList, outWeight)):
    for j, weight in zip(out_nodes, weights):
        G.add_edge(i, j, weight=weight)

# Calculate viral centrality
tol = 0.001
num_activated = viral_centrality(inList, inWeight, outList, Niter=-1, tol=tol)

# Calculate centrality measures
degree_centrality = nx.degree_centrality(G)
betweenness_centrality = nx.betweenness_centrality(G, weight='weight')
closeness_centrality = nx.closeness_centrality(G, distance='weight')

# Increase max_iter and adjust tolerance for eigenvector centrality
try:
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06, weight='weight')
except nx.PowerIterationFailedConvergence:
    print("Power iteration failed to converge for eigenvector centrality")

# Convert centrality measures to lists
degree_centrality_values = [degree_centrality[node] for node in G.nodes]
betweenness_centrality_values = [betweenness_centrality[node] for node in G.nodes]
closeness_centrality_values = [closeness_centrality[node] for node in G.nodes]
eigenvector_centrality_values = [eigenvector_centrality[node] for node in G.nodes] if 'eigenvector_centrality' in locals() else [0] * len(G.nodes)

# Correlation analysis
correlations = {
    'Degree Centrality': pearsonr(degree_centrality_values, num_activated),
    'Betweenness Centrality': pearsonr(betweenness_centrality_values, num_activated),
    'Closeness Centrality': pearsonr(closeness_centrality_values, num_activated),
    'Eigenvector Centrality': pearsonr(eigenvector_centrality_values, num_activated)
}

# Plot results
plt.figure(figsize=(12, 8))
plt.subplot(2, 2, 1)
plt.scatter(degree_centrality_values, num_activated, color='blue', label='Degree Centrality')
plt.xlabel('Degree Centrality', fontsize=12)
plt.ylabel('Avg Number Activated', fontsize=12)
plt.legend()

plt.subplot(2, 2, 2)
plt.scatter(betweenness_centrality_values, num_activated, color='green', label='Betweenness Centrality')
plt.xlabel('Betweenness Centrality', fontsize=12)
plt.ylabel('Avg Number Activated', fontsize=12)
plt.legend()

plt.subplot(2, 2, 3)
plt.scatter(closeness_centrality_values, num_activated, color='red', label='Closeness Centrality')
plt.xlabel('Closeness Centrality', fontsize=12)
plt.ylabel('Avg Number Activated', fontsize=12)
plt.legend()

plt.subplot(2, 2, 4)
plt.scatter(eigenvector_centrality_values, num_activated, color='purple', label='Eigenvector Centrality')
plt.xlabel('Eigenvector Centrality', fontsize=12)
plt.ylabel('Avg Number Activated', fontsize=12)
plt.legend()

plt.suptitle('Influence of Centrality Measures on Information Spread', fontsize=16)
plt.tight_layout(rect=[0, 0, 1, 0.96])
plt.savefig('centrality_influence.pdf')

plt.show()


# Print correlation results
for centrality, (correlation, p_value) in correlations.items():
    print(f'Correlation between {centrality} and number activated: {correlation}')
    print(f'P-value: {p_value}')