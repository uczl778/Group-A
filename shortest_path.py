import networkx as nx


class shortest_path():

    def __init__(self, start_point, end_point, iow_itn, dataset):
        self.start_point = start_point
        self.end_point = end_point
        self.iow_itn = iow_itn
        self.dataset = dataset
        self.matrix = self.dataset.read(1)

    def calculate_elevation(self, coor1, coor2):

        x1 = coor1[0]
        y1 = coor1[1]

        x2 = coor2[0]
        y2 = coor2[1]

        row, col = self.dataset.index(x1, y1)
        h1 = self.matrix[row, col]
        row, col = self.dataset.index(x2, y2)
        h2 = self.matrix[row, col]
        elevation = abs(h1 - h2)
        return elevation

    def g_map(self):
        # 5km/hr = 5000m/60min
        # elevation: 1min/10 meters
        g = nx.Graph()
        links = self.iow_itn['roadlinks']
        nodes = self.iow_itn['roadnodes']
        # extremely long running time here !!!
        for index, link in enumerate(links):
            if index % 30 == 0:
                print(index, '/', len(links))
            pt1 = links[link]['start']
            pt2 = links[link]['end']
            elevation = self.calculate_elevation(nodes[pt1]['coords'], nodes[pt2]['coords'])
            g.add_edge(links[link]['start'], links[link]['end'], fid=link,
                       weight=links[link]['length'] / 5000 * 60 + elevation * 1 / 10)
        return g

    def shortest_path(self, g):
        path = nx.dijkstra_path(g, source=self.start_point, target=self.end_point, weight="weight")
        return path

