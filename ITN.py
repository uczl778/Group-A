from rtree import *
import networkx as nx
import json

idx = index.Index()
br = (430000, 80000, 465000, 95000)
idx.insert(0, br)
for i in range(1000):
    for j in range(1000):
        idx.insert(i * 1000 + j, (i, j, i + 10, j + 10))
for i in idx.intersection((1.0, 1.0, 2.0, 2.0)):
    print(i)
for i in idx.nearest((0.8, 0.8), 1):
    print(i)

g = nx.Graph()
solent_itn_json = "E:/pycharm/ass2/Material/itn/solent_itn.json"
with open(solent_itn_json, "r") as f:
    solent_itn = json.load(f)

g = nx.Graph()
road_links = solent_itn['roadlinks']
for link in road_links:
    g.add_edge(road_links[link]['start'], road_links[link]['end'], fid=link, weight=road_links[link]['length'])
