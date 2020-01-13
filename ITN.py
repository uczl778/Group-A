from rtree import index
import networkx as nx
import json

idx = index.Index()


def itn(x, y):
    global nearest_node
    solent_itn_json = "E:/pycharm/ass2/Material/itn/solent_itn.json"
    with open(solent_itn_json, "r") as load_f:
        solent_itn = json.load(load_f)

    road_nodes = solent_itn['roadnodes']

    index = 0
    # create a list for node id
    node_append_coords = []
    node_list = {}

    for road_id in road_nodes:
        # node_coords = road_nodes[road_id]['coords']
        node = road_nodes[road_id]['coords']
        idx.insert(index, (node[0], node[1], node[0], node[1]))

        node_list[index] = road_id
        index = index + 1


    # find out the nearest node from user
    for i in idx.nearest((x, y), 1):
        nearest_node = node_list[i]
        # nearest_id = node_list[i][index]

    return nearest_node