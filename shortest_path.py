import json
import os
from rasterio import plot
import numpy as np
from rtree import index
import networkx as nx
import rasterio
import pyproj
import geopandas as gpd
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import *



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

    # #  use the color_path function that we created earlier to color the graph network and then plot it
    # def color_path(self, g, path, color="blue"):
    #     res = g.copy()
    #     first = path[0]
    #     for node in path[1:]:
    #         res.edges[first, node]["color"] = color
    #         first = node
    #     return res

    # def obtain_colors(self, graph, default_node="blue", default_edge="black"):
    #     node_colors = []
    #     for node in graph.nodes:
    #         node_colors.append(graph.nodes[node].get('color', default_node))
    #     edge_colors = []
    #     for u, v in graph.edges:
    #         edge_colors.append(graph.edges[u, v].get('color', default_edge))
    #     return node_colors, edge_colors
    #
    # def visual_path(self, g, path, background):
    #     g_1 = self.color_path(g, path, "red")
    #     node_colors, edge_colors = self.obtain_colors(g_1)
    #
    #     nx.draw(g_1, node_size=1, edge_color=edge_colors, node_color=node_colors)
    #
    #     # append the feature id and the geometry to two lists links and geom which are used to build the path_gpd GeoDataFrame.
    #     links = self.iow_itn['roadlinks']
    #     links_g = []
    #     geom = []
    #     first_node = path[0]
    #     for node in path[1:]:
    #         link_fid = g.edges[first_node, node]['fid']
    #         links_g.append(link_fid)
    #         geom.append(LineString(links[link_fid]['coords']))
    #         first_node = node
    #
    #     shortest_path_gpd = gpd.GeoDataFrame({"fid": links_g, "geometry": geom})
    #     shortest_path_gpd.plot()
    #
    #     #  view the route, apply the colormap to the array
    #     back_array = background.read(1)
    #     palette = np.array([value for key, value in background.colormap(1).items()])
    #     background_image = palette[back_array]
    #     bounds = background.bounds
    #     extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
    #     display_extent = [bounds.left + 200, bounds.right - 200, bounds.bottom + 600, bounds.top - 600]
    #
    #     fig = plt.figure(figsize=(3, 3), dpi=300)
    #     ax = fig.add_subplot(1, 1, 1, projection=ccrs.OSGB())
    #
    #     ax.imshow(background_image, origin="upper", extent=extent, zorder=0)
    #     shortest_path_gpd.plot(ax=ax, edgecolor="blue", linewidth=0.5, zorder=2)
    #     ax.set_extent(display_extent, crs=ccrs.OSGB())


# test
# temp = shortest_path(start, end, iow_itn, dataset)
# g_map = temp.g_map()
# path = temp.shorest_path(g_map)
# temp.visual_path(g_map, path, background)
