import matplotlib.font_manager as fm
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
from matplotlib import colors
import matplotlib
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from shapely.geometry import *
from rasterio.mask import mask
from rasterio.plot import *
import geopandas as gpd

matplotlib.use('TkAgg')


class Plotter:

    def __init__(self, pt_user, pt_highest, background, elevation, graph, path, iow_itn):
        self.__pt_user = pt_user
        self.__pt_highest = pt_highest
        self.__background = background
        self.__elevation = elevation
        self.__graph = graph
        self.__path = path
        self.__iow_itn = iow_itn

    def get_pt_user(self):
        return self.__pt_user

    def get_pt_highest(self):
        return self.__pt_highest

    def get_elevation(self):
        return self.__elevation

    def get_graph(self):
        return self.__graph

    def get_path(self):
        return self.__path

    def get_background(self):
        return self.__background

    def get_iow_itn(self):
        return self.__iow_itn

    def visual_path(self):
        g = self.get_graph()
        path = self.get_path()
        background = self.get_background()
        iow_itn = self.get_iow_itn()
        pt_user = self.get_pt_user()
        pt_highest = self.get_pt_highest()
        elevation = self.get_elevation()

        # Append the feature id and the geometry to two lists links and geom which are used to build the path_gpd
        # GeoDataFrame.
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
        # shortest_path_gpd.plot()

        # Make a figure
        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=ccrs.OSGB())

        # Clip and plot the background
        win_back = background.read(1)

        palette = np.array([value for key, value in background.colormap(1).items()])
        background_image = palette[win_back]

        left, bottom, right, top = background.bounds.left, background.bounds.bottom, background.bounds.right, background.bounds.top
        extent = [left, right, bottom, top]
        display_extent = [pt_user.x + 7500, pt_user.x - 7500, pt_user.y + 7500, pt_user.y - 7500]

        ax.imshow(background_image, origin="upper", extent=extent, zorder=0)

        # Clip and plot the elevation
        buffered_zone = pt_user.buffer(5000)
        buffer_ele, buffer_transform = mask(elevation, [buffered_zone], crop=True, nodata=np.nan)

        elevation_image = buffer_ele[0]
        left_bottom2 = (0, 0)
        right_top2 = (elevation_image.shape[1], elevation_image.shape[0])
        left2, top2 = buffer_transform * left_bottom2
        right2, bottom2 = buffer_transform * right_top2
        extent2 = [left2, right2, bottom2, top2]

        ele_img = ax.imshow(elevation_image, origin="upper", extent=extent2, alpha=0.6, zorder=1, vmin=0,
                            cmap='terrain')

        # Plot the shortest path
        shortest_path_gpd.plot(ax=ax, edgecolor="blue", linewidth=0.5, zorder=2, label="Shortest_path")
        ax.set_extent(display_extent, crs=ccrs.OSGB())

        # Plot the starting point and the highest point
        plt.plot(pt_user.x, pt_user.y, "ro", markersize=2, label="Starting_point")
        plt.plot(pt_highest.x, pt_highest.y, "go", markersize=2, label="Highest_point")

        # Add a color-bar for the elevation buffer
        cbar = fig.colorbar(ele_img, cmap='terrain', ax=ax, shrink=0.8,
                            norm=colors.Normalize(vmin=np.nanmin(elevation_image), vmax=np.nanmax(elevation_image)))
        cbar.ax.tick_params(labelsize=3)
        # Add a North Arrow
        arrow_x, arrow_y, arrow_length = 0.05, 0.95, 0.1
        ax.annotate('N', xy=(arrow_x, arrow_y), xytext=(arrow_x, arrow_y - arrow_length),
                    arrowprops=dict(facecolor='black', width=1, headwidth=3, headlength=3),
                    ha='center', va='center', fontsize=5,
                    xycoords=ax.transAxes)

        # Add a legend
        plt.legend(loc='upper right', fontsize=3)

        # Add a scale bar
        fontprops = fm.FontProperties(size=5)
        scalebar = AnchoredSizeBar(ax.transData,
                                   2000, '2km', 3,
                                   pad=0.1,
                                   color='Black',
                                   frameon=False,
                                   size_vertical=1,
                                   fontproperties=fontprops)

        ax.add_artist(scalebar)

        # Show the result map
        plt.show()
