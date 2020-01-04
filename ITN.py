from rtree import index
import networkx as nx
import json

solent_itn_json = "E:/pycharm/ass2/Material/itn/solent_itn.json"
with open('solent_itn.json', "r") as load_f:
    solent_itn = json.load(load_f)

#create the bounding box
idx = index.Index()
index = 0
idx.insert(index,(430000,465000,80000,95000))
index = index + 1

road_nodes = solent_itn['roadnodes']
idx = list(road_nodes)
#create a list of the coords
road_nodes = []

for coords in road_nodes:
    node_coords = road_nodes[road_id]['coords']
    road_nodes.append(coords(1,node_coords))

road_links = solent_itn['roadlinks']
for link in roadlinks:

# firstnode = [0,0]
# endnode = [3,3]

previousnode = start
for node in coords:
    idx.insert(index, (firstnode[0], firstnode[1],node[0], node[1]))
    previousnode = node
    index = index + 1

for i in range(100):
    for j in range(100):
        idx.insert(i*100 + j, (i, j, i+0.99, j+0.99))

for i in idx.intersection((x - 5000, y - 5000, x + 5000, y +5000)):
    # User-centered rectangle with a radius of 5 kilometers
    print(i)

for i in idx.nearest((x, y), 1):
    #（x，y） user's coordinate
    print(i)














