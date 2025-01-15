import json
import networkx as nx
import matplotlib.pyplot as plt

# Load the JSON dataset
with open('congress_network_data.json', 'r') as f:
    data = json.load(f)

# Extract data from JSON
inList = data['inList']
inWeight = data['inWeight']
outList = data['outList']
outWeight = data['outWeight']
usernameList = data['usernameList']

# Create a directed graph
G = nx.DiGraph()

# Add nodes with labels
for i, username in enumerate(usernameList):
    G.add_node(i, label=username)

# Add edges with weights from JSON data
for i, out_nodes in enumerate(outList):
    for j, target in enumerate(out_nodes):
        G.add_edge(i, target, weight=outWeight[i][j])

# Manually parse the edge list file and add edges to the graph
with open('congress.edgelist', 'r') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            source = int(parts[0])
            target = int(parts[1])
            weight = float(parts[2].split(':')[1].strip('}'))
            G.add_edge(source, target, weight=weight)

# Draw the graph
pos = nx.spring_layout(G)  # Position nodes using Fruchterman-Reingold force-directed algorithm
plt.figure(figsize=(12, 12))

# Draw nodes
nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')

# Draw edges
nx.draw_networkx_edges(G, pos, arrowstyle='->', arrowsize=10, edge_color='gray')

# Draw labels
nx.draw_networkx_labels(G, pos, labels=nx.get_node_attributes(G, 'label'), font_size=10)

plt.title('Congressional Twitter Network')
plt.show()