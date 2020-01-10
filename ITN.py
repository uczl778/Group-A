from rtree import index
import networkx as nx
import json

solent_itn_json = "E:/pycharm/ass2/Material/itn/solent_itn.json"
with open('solent_itn.json', "r") as load_f:
    solent_itn = json.load(load_f)

road_nodes = solent_itn['roadnodes']

idx = index.Index()
index = 0
# create a list for node id
noad_append_id = []
for coords in road_nodes:
    node_coords = road_nodes[coords]['coords']
    road_id = coords
    noad_append_id.append(node_coords)
print(noad_append_id)

for node in noad_append_id:
     idx.insert(index, (node[0], node[1], node[0], node[1]))
     index = index + 1
# Let the user enter x,y coordinates
x = 442798
y = 75320
# find out the nearest node from user
for i in idx.nearest((x, y), 1):
       print(i)

