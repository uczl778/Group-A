from rtree import index
import networkx as nx
import json
idx = index.Index()
def  itn(x, y):
    solent_itn_json = "E:/pycharm/ass2/Material/itn/solent_itn.json"
    with open('solent_itn.json', "r") as load_f:
        solent_itn = json.load(load_f)

    road_nodes = solent_itn['roadnodes']

    index = 0
    # create a list for node id
    node_append_id = []
    for coords in road_nodes:
        node_coords = road_nodes[coords]['coords']
        road_id = coords

        node_append_id.append(node_coords)
    print(node_append_id)

    for node in node_append_id:
         idx.insert(index, (node[0], node[1], node[0], node[1]))
         index = index + 1
    # Let the user enter x,y coordinates

    # find out the nearest node from user
    for i in idx.nearest((x, y), 1):
        nearest_node = node_append_id[i]
        return node_append_id[i]






