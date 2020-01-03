from rtree import *
import networkx as nx
import json

solent_itn_json = "E:/pycharm/ass2/Material/itn/solent_itn.json"
with open('solent_itn.json', "r") as load_f:
    #print(load_dict['roadlinks'])
    solent_itn = json.load(load_f)
#get the road id
road_nodes = solent_itn['roadnodes']
for road_id in road_nodes:
    node_coords = road_nodes[road_id]['coords']
    print(node_coords)
#print(load_dict[''][1])


idx = index.Index()
br = (1, 1, 20, 20)
idx.insert(0, br)
for i in range(1000):
    for j in range(1000):
        idx.insert(i * 1000 + j, (i, j, i + 10, j + 10))
for i in idx.intersection((1.0, 1.0, 20.0, 20.0)):
     print(i)
for i in idx.nearest((20,20), 1):
     print(i)



