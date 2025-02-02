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
try:
    eigenvector_centrality = nx.eigenvector_centrality(G, max_iter=1000, tol=1e-06, weight='weight')
except nx.PowerIterationFailedConvergence:
    eigenvector_centrality = {node: 0 for node in G.nodes}

# Compute viral centrality inline
tol = 0.001
viral_centrality_values = viral_centrality(inList, inWeight, outList, Niter=-1, tol=tol)

# Debugging: Print viral centrality values
print("Viral Centrality Values:", viral_centrality_values)

def get_ranking_from_dict(dct):
    return sorted(dct, key=dct.get, reverse=True)

def get_ranking_from_list(lst):
    return sorted(range(len(lst)), key=lambda i: lst[i], reverse=True)

eigenvector_ranking = get_ranking_from_dict(eigenvector_centrality)
viral_ranking = get_ranking_from_list(viral_centrality_values)

# Compute weighted PageRank centrality
def weighted_pagerank_centrality(G, alpha=0.85, max_iter=100, tol=1.0e-6):
    import math

    N = len(G)
    if N == 0:
        return {}

    pr = {node: 1.0 / N for node in G.nodes()}

    out_strength = {}
    for node in G.nodes():
        total_weight_out = 0.0
        for nbr in G.successors(node):
            total_weight_out += G[node][nbr].get('weight', 0.0)
        out_strength[node] = total_weight_out

    for _ in range(max_iter):
        prev_pr = pr.copy()
        for node in pr:
            pr[node] = (1.0 - alpha) / N

        for node in G.nodes():
            if out_strength[node] == 0:
                for n2 in pr:
                    pr[n2] += alpha * (prev_pr[node] / N)
            else:
                for nbr in G.successors(node):
                    w = G[node][nbr].get('weight', 0.0)
                    pr[nbr] += alpha * (prev_pr[node] * (w / out_strength[node]))

        diff = sum(abs(pr[n] - prev_pr[n]) for n in pr)
        if diff < tol:
            break

    return pr

weighted_pagerank = weighted_pagerank_centrality(G)
weighted_pagerank_ranking = get_ranking_from_dict(weighted_pagerank)

# Compute probabilistic centralities
def prob_degree_centrality(G):
    centrality = {}
    for node in G.nodes():
        out_prob = sum(G[node][nbr]['weight'] for nbr in G.successors(node))
        in_prob = sum(G[pred][node]['weight'] for pred in G.predecessors(node))
        centrality[node] = out_prob + in_prob
    return centrality

def prob_betweenness_centrality(G):
    from collections import defaultdict
    import math

    betweenness = defaultdict(float)
    nodes = list(G.nodes())
    
    log_w = {}
    for u, v in G.edges():
        log_w[(u, v)] = math.log(G[u][v]['weight']) if G[u][v]['weight'] > 0 else float('-inf')

    for s in nodes:
        dist = {n: float('inf') for n in nodes}
        predecessor = {n: None for n in nodes}
        dist[s] = 0
        
        unvisited = set(nodes)
        while unvisited:
            current = min(unvisited, key=lambda x: dist[x])
            unvisited.remove(current)
            if dist[current] == float('inf'):
                break
            for nbr in G.successors(current):
                cost = dist[current] + (-log_w.get((current, nbr), float('-inf')))
                if cost < dist[nbr]:
                    dist[nbr] = cost
                    predecessor[nbr] = current
        
        for t in nodes:
            if t == s or dist[t] == float('inf'):
                continue
            path_nodes = []
            cur = t
            while cur is not None:
                path_nodes.append(cur)
                cur = predecessor[cur]
            path_nodes.reverse()
            for n in path_nodes:
                betweenness[n] += 1
    
    return dict(betweenness)

def prob_closeness_centrality(G):
    import math
    
    closeness = {}
    nodes = list(G.nodes())

    log_w = {}
    for u, v in G.edges():
        log_w[(u, v)] = -math.log(G[u][v]['weight']) if G[u][v]['weight'] > 0 else float('inf')

    for s in nodes:
        dist = {n: float('inf') for n in nodes}
        dist[s] = 0
        visited = set()
        while len(visited) < len(nodes):
            current = min((x for x in nodes if x not in visited), key=lambda x: dist[x])
            visited.add(current)
            if dist[current] == float('inf'):
                break
            for nbr in G.successors(current):
                d = dist[current] + log_w.get((current, nbr), float('inf'))
                if d < dist[nbr]:
                    dist[nbr] = d
        total = sum(x for x in dist.values() if x < float('inf'))
        if total > 0 and total < float('inf'):
            closeness[s] = (len(nodes) - 1) / total
        else:
            closeness[s] = 0.0

    return closeness

prob_degree = prob_degree_centrality(G)
prob_betweenness = prob_betweenness_centrality(G)
prob_closeness = prob_closeness_centrality(G)

prob_degree_ranking = get_ranking_from_dict(prob_degree)
prob_betweenness_ranking = get_ranking_from_dict(prob_betweenness)
prob_closeness_ranking = get_ranking_from_dict(prob_closeness)

# Compare top 10% rankings using Kendall's Tau
rankings = {
    'Eigenvector Centrality': eigenvector_ranking,
    'Viral Centrality': viral_ranking,
    'Weighted PageRank': weighted_pagerank_ranking,
    'Prob Degree Centrality': prob_degree_ranking,
    'Prob Betweenness Centrality': prob_betweenness_ranking,
    'Prob Closeness Centrality': prob_closeness_ranking
}

# Extract top 10% from ground truth ranking
top_10_percent_index = int(len(ground_truth_ranking) * 0.1)
top_10_percent_ground_truth = ground_truth_ranking[:top_10_percent_index]

results = []
for name, ranking in rankings.items():
    top_10_percent_ranking = ranking[:top_10_percent_index]
    tau, p_value = kendalltau(top_10_percent_ranking, top_10_percent_ground_truth)
    results.append([name, tau, p_value])
    print(f"Kendall's Tau between {name} and ground truth ranking (Top 10%): {tau:.3f}")
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
print("Eigenvector Centrality Ranking (Top 10%):", eigenvector_ranking[:top_10_percent_index])
print("Viral Centrality Ranking (Top 10%):", viral_ranking[:top_10_percent_index])
print("Weighted PageRank Ranking (Top 10%):", weighted_pagerank_ranking[:top_10_percent_index])
print("Prob Degree Centrality Ranking (Top 10%):", prob_degree_ranking[:top_10_percent_index])
print("Prob Betweenness Centrality Ranking (Top 10%):", prob_betweenness_ranking[:top_10_percent_index])
print("Prob Closeness Centrality Ranking (Top 10%):", prob_closeness_ranking[:top_10_percent_index])
print("Ground Truth Ranking (Top 10%):", top_10_percent_ground_truth)




