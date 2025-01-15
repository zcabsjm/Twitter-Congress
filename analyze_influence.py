import json
import numpy as np
import networkx as nx
import pandas as pd
from matplotlib import pyplot as plt
from scipy.stats import kendalltau
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
def run_icm_simulation(G, num_simulations=10000):
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
num_simulations = 10000  # Reduced to 1000 for debugging
avg_spread = run_icm_simulation(G, num_simulations)
ground_truth_ranking = sorted(avg_spread, key=avg_spread.get, reverse=True)

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

def get_ranking_from_dict(dct):
    return sorted(dct, key=dct.get, reverse=True)

def get_ranking_from_list(lst):
    return sorted(range(len(lst)), key=lambda i: lst[i], reverse=True)

degree_ranking = get_ranking_from_dict(degree_centrality)
betweenness_ranking = get_ranking_from_dict(betweenness_centrality)
closeness_ranking = get_ranking_from_dict(closeness_centrality)
eigenvector_ranking = get_ranking_from_dict(eigenvector_centrality)
viral_ranking = get_ranking_from_list(viral_centrality_values)

# Compare top 10 rankings using Kendall's Tau
rankings = {
    'Degree Centrality': degree_ranking,
    'Betweenness Centrality': betweenness_ranking,
    'Closeness Centrality': closeness_ranking,
    'Eigenvector Centrality': eigenvector_ranking,
    'Viral Centrality': viral_ranking
}

# Extract top 10 from ground truth ranking
top_10_ground_truth = ground_truth_ranking[:10]

results = []
for name, ranking in rankings.items():
    top_10_ranking = ranking[:10]
    tau, p_value = kendalltau(top_10_ranking, top_10_ground_truth)
    results.append([name, tau, p_value])
    print(f"Kendall's Tau between {name} and ground truth ranking (Top 10): {tau:.3f}")
    print(f"P-value: {p_value:.3g}")

# Create a DataFrame for the results
df_results = pd.DataFrame(results, columns=['Centrality Measure', 'Kendall\'s Tau', 'P-value'])

# Save the DataFrame as a table in a PDF
fig, ax = plt.subplots(figsize=(8, 4))  # Set the size of the figure
ax.axis('tight')
ax.axis('off')
table = ax.table(cellText=df_results.values, colLabels=df_results.columns, cellLoc='center', loc='center')
table.auto_set_font_size(False)
table.set_fontsize(10)
table.scale(1.2, 1.2)  # Adjust the scale of the table

plt.savefig('centrality_kendall_tau_results.pdf', bbox_inches='tight')

# Debugging Print Statements
print("Degree Centrality Ranking (Top 10):", degree_ranking[:10])
print("Betweenness Centrality Ranking (Top 10):", betweenness_ranking[:10])
print("Closeness Centrality Ranking (Top 10):", closeness_ranking[:10])
print("Eigenvector Centrality Ranking (Top 10):", eigenvector_ranking[:10])
print("Viral Centrality Ranking (Top 10):", viral_ranking[:10])
print("Ground Truth Ranking (Top 10):", top_10_ground_truth)




