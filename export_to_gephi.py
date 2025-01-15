import json
import networkx as nx

# Load the JSON dataset
with open('congress_network_data.json', 'r') as f:
    data = json.load(f)

# Debugging: Print the type and first element of the loaded data
print("Type of loaded data:", type(data))
print("First element of the loaded data:", data[0])

# Extract data from the first element of the list
data_dict = data[0]  # Assuming the first element is the dictionary we need
inList = data_dict['inList']
inWeight = data_dict['inWeight']
outList = data_dict['outList']
outWeight = data_dict['outWeight']
usernameList = data_dict['usernameList']

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

# Export the graph to a GEXF file
nx.write_gexf(G, 'congress_network.gexf')

print("Graph exported to congress_network.gexf")