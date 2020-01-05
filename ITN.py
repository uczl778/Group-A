from rtree import index
import networkx as nx
import json

solent_itn_json = "E:/pycharm/ass2/Material/itn/solent_itn.json"
with open('solent_itn.json', "r") as load_f:
    solent_itn = json.load(load_f)

#create the bounding box

# idx.insert(index,(430000,80000,465000,95000))
# index = index + 1

road_nodes = solent_itn['roadnodes']
# idx = list(road_nodes)
# print(idx)
#create a list of the coords
# noad_list = {}
idx = index.Index()
index = 0
noad_append_test = []

for coords in road_nodes:
    node_coords = road_nodes[coords]['coords']
    road_id = coords
    # noad_list[road_id] = node_coords
    noad_append_test.append(node_coords)
print(noad_append_test)

# road_links = solent_itn['roadlinks']

#firstnode = noad_append_test[0]
#print(firstnode)
# endnode = [3,3]

#previousnode = firstnode
for node in noad_append_test:
     idx.insert(index, (node[0], node[1], node[0], node[1]))
     #previousnode = node
     index = index + 1



# for i in range(100):
#     for j in range(100):
#         idx.insert(i*100 + j, (i, j, i+0.99, j+0.99))
#
#print(list(idx.intersection((442798, 75320, 452798, 85320))))
# for i in set(idx.intersection((442798, 75320, 452798, 85320))):
    # User-centered rectangle with a radius of 5 kilometers
    # print(i)

x = 442798
y = 75320

for i in idx.nearest((x, y), 1):
    #（x，y） user's coordinate
    print(i)

print(noad_append_test[2288])