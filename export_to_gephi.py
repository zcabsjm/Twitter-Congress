import json
import networkx as nx

with open('congress_network_data.json', 'r') as f:
    data = json.load(f)

data_dict = data[0]  
inList = data_dict['inList']
inWeight = data_dict['inWeight']
outList = data_dict['outList']
outWeight = data_dict['outWeight']
usernameList = data_dict['usernameList']

G = nx.DiGraph()

# Add nodes with labels
for i, username in enumerate(usernameList):
    G.add_node(i, label=username)

for i, out_nodes in enumerate(outList):
    for j, target in enumerate(out_nodes):
        G.add_edge(i, target, weight=outWeight[i][j])

with open('congress.edgelist', 'r') as f:
    for line in f:
        parts = line.strip().split()
        if len(parts) == 3:
            source = int(parts[0])
            target = int(parts[1])
            weight = float(parts[2].split(':')[1].strip('}'))
            G.add_edge(source, target, weight=weight)

nx.write_gexf(G, 'congress_network.gexf')

print("Graph exported to congress_network.gexf")