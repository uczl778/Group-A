from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt
import rasterio
from rasterio import plot
import numpy as np
import cartopy.crs as ccrs
from shapely.geometry import *
from rasterio.mask import mask
from rasterio.windows import Window
from rasterio.plot import *
import networkx as nx
import geopandas as gpd

matplotlib.use('TkAgg')


class Plotter:

    def __init__(self, pt_user, pt_highest, graph, path, background, iow_itn):
        self.__pt_user = pt_user
        self.__pt_highest = pt_highest
        self.__graph = graph
        self.__path = path
        self.__background = background
        self.__iow_itn = iow_itn

    def get_pt_user(self):
        return self.__pt_user

    def get_pt_highest(self):
        return self.__pt_highest

    def get_graph(self):
        return self.__graph

    def get_path(self):
        return self.__path

    def get_background(self):
        return self.__background

    def get_iow_itn(self):
        return self.__iow_itn

    #  use the color_path function that we created earlier to color the graph network and then plot it
    def color_path(self, color="blue"):
        g = self.get_graph()
        path = self.get_path()

        res = g.copy()
        first = path[0]
        for node in path[1:]:
            res.edges[first, node]["color"] = color
            first = node
        return res

    def obtain_colors(self, default_node="blue", default_edge="black"):
        graph = self.get_graph()

        node_colors = []
        for node in graph.nodes:
            node_colors.append(graph.nodes[node].get('color', default_node))
        edge_colors = []
        for u, v in graph.edges:
            edge_colors.append(graph.edges[u, v].get('color', default_edge))
        return node_colors, edge_colors

    def visual_path(self):
        g = self.get_graph()
        path = self.get_path()
        background = self.get_background()
        iow_itn = self.get_iow_itn()
        pt_user = self.get_pt_user()
        pt_highest = self.get_pt_highest()

        g_1 = self.color_path("red")
        node_colors, edge_colors = self.obtain_colors(g_1)

        nx.draw(g_1, node_size=1, edge_color=edge_colors, node_color=node_colors)

        # append the feature id and the geometry to two lists links and geom which are used to build the path_gpd GeoDataFrame.
        links = iow_itn['roadlinks']
        links_g = []
        geom = []
        first_node = path[0]
        for node in path[1:]:
            link_fid = g.edges[first_node, node]['fid']
            links_g.append(link_fid)
            geom.append(LineString(links[link_fid]['coords']))
            first_node = node

        shortest_path_gpd = gpd.GeoDataFrame({"fid": links_g, "geometry": geom})
        shortest_path_gpd.plot()

        #  view the route, apply the colormap to the array


        # back_array = background.read(1)
        # palette = np.array([value for key, value in background.colormap(1).items()])
        # background_image = palette[back_array]
        # bounds = background.bounds
        # extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        # display_extent = [bounds.left + 200, bounds.right - 200, bounds.bottom + 600, bounds.top - 600]


        # Plot the background window
        r_u, c_u = background.index(pt_user.x, pt_user.y)
        win = Window(r_u - 2000, c_u - 2000, 4000, 4000)
        win_back = background.read(1, window=win)
        win_transform = background.window_transform(win)

        palette = np.array([value for key, value in background.colormap(1).items()])
        background_image = palette[win_back]
        bounds = win_back.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        display_extent = win_transform * extent

        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.OSGB())

        ax.imshow(background_image, origin="upper", extent=extent, zorder=0)
        shortest_path_gpd.plot(ax=ax, edgecolor="blue", linewidth=0.5, zorder=2)
        ax.set_extent(display_extent, crs=ccrs.OSGB())

        # plt.matshow(win_back)

        # Plot the starting point and the highest point
        plt.plot(pt_user.x, pt_user.y, "ro", label="Starting_point")
        plt.plot(pt_highest.x, pt_highest.y, "go", label="Highest_point")

        # # Plot the legend
        # handles, labels = plt.gca().get_legend_handles_labels()
        # by_label = OrderedDict(zip(labels, handles))
        # plt.legend(by_label.values(), by_label.keys())
        plt.show()
