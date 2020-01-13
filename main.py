from collections import OrderedDict
import matplotlib.font_manager as fm
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib
from matplotlib import colors
import matplotlib.cbook as cbook
from shapely.geometry import *
from pyproj import *
import rasterio
import sys
from highest_pt import *
from shortest_path import *
from plotter import *
import geopandas as gpd
from rasterio.mask import mask
from ITN import *
import cartopy
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from rasterio.windows import Window

matplotlib.use('TkAgg')


def main():
    # Task1: User Input
    tuple_user = (439619, 85800)
    # tuple_user = (sys.argv[1], sys.argv[2])
    # Error handling
    try:
        x = float(tuple_user[0])
        y = float(tuple_user[1])
    except ValueError:
        print("The coordinate should be number, please input again: ")
        while True:
            try:
                x = float(input("x coordinate: "))
                y = float(input("y coordinate: "))
                break
            except ValueError:
                print("The coordinate should be number, please input again: ")
    pt_user = Point(x, y)

    # Test whether the user is within the box
    min_x = 430000
    max_x = 465000
    min_y = 80000
    max_y = 95000
    if pt_user.x > max_x or pt_user.x < min_x or pt_user.y > max_y or pt_user.y < min_y:
        print("The user is outside this box. ")
        sys.exit()

    # Task2: Highest Point Identification
    # Read the elevation
    ele_fp = 'E:/pycharm/ass2/Material/elevation/SZ.asc'
    elevation = rasterio.open(ele_fp)
    # Create an object of the highest point
    point_highest = highest_pt(pt_user, elevation)
    pt_highest, max_ele, buffer_ele = point_highest.get_highest_pt()

    print("The coordinate of the highest point is: " + str(pt_highest.x) + ", " + str(pt_highest.y))
    print("The elevation of the highest point is: " + str(max_ele))

    # Task 3: Nearest Integrated Transport Network
    node_user_id = itn(pt_user.x, pt_user.y)
    print(itn(pt_user.x, pt_user.y))
    node_highest_id = itn(pt_highest.x, pt_highest.y)
    print(itn(pt_highest.x, pt_highest.y))

    # Task 4: Shortest Path
    # Read the network
    iow_itn_json = "E:/pycharm/ass2/Material/itn/solent_itn.json"
    with open(iow_itn_json, "r") as f:
        iow_itn = json.load(f)
    # Read the elevation info
    dataset = elevation
    # View the route, load the background map
    mersea_background = "E:/pycharm/ass2/Material/background/raster-50k_2724246.tif"
    background = rasterio.open(str(mersea_background))
    # The start point and end point
    start = node_user_id
    end = node_highest_id
    # Create an object of the shortest path
    path_shortest = shortest_path(start, end, iow_itn, dataset)
    g_map = path_shortest.g_map()
    path = path_shortest.shortest_path(g_map)
    # path_shortest.visual_path(g_map, path, background)

    # Task 5: Map Plotting

    plotter = Plotter(pt_user, pt_highest, background, elevation, g_map, path, iow_itn)
    plotter.visual_path()

    # # Make a figure
    # fig = plt.figure(figsize=(3, 3), dpi=300)
    # ax = fig.add_subplot(1, 1, 1, projection=ccrs.OSGB())

    # # Clip and plot the background
    # r_u, c_u = background.index(pt_user.x, pt_user.y)
    # win = Window(r_u - 2000, c_u - 2000, 4000, 4000)
    # win_back = background.read(1, window=win)
    # win_transform = background.window_transform(win)
    #
    # palette = np.array([value for key, value in background.colormap(1).items()])
    # background_image = palette[win_back]
    # left_bottom = (0, 0)
    # right_top = (win_back.shape[1], win_back.shape[0])
    # # bounds = win_back.bounds
    # left, top = win_transform * left_bottom
    # right, bottom = win_transform * right_top
    # # left, right, bottom, top = win_transform * (pt1.x, pt2.x, pt1.y, pt2.y)
    # extent = [left, right, bottom, top]
    # display_extent = [left + 200, right - 200, bottom + 600, top - 600]
    #
    # ax.imshow(background_image, origin="upper", extent=extent, zorder=0)

    # # Clip and plot the elevation
    # buffered_zone = pt_user.buffer(5000)
    # buffer_ele, buffer_transform = mask(elevation, [buffered_zone], crop=True, nodata=np.nan)
    #
    # elevation_image = buffer_ele[0]
    # left_bottom2 = (0, 0)
    # right_top2 = (elevation_image.shape[1], elevation_image.shape[0])
    # left2, top2 = buffer_transform * left_bottom2
    # right2, bottom2 = buffer_transform * right_top2
    # extent2 = [left2, right2, bottom2, top2]
    #
    # ele_img = ax.imshow(elevation_image, origin="upper", extent=extent2, alpha=0.6, zorder=1, vmin=0, cmap='terrain')

    # # Plot the shortest path
    # # shortest_path_gpd.plot(ax=ax, edgecolor="blue", linewidth=0.5, zorder=2)
    # ax.set_extent(display_extent, crs=ccrs.OSGB())

    # # Plot the starting point and the highest point
    # plt.plot(pt_user.x, pt_user.y, "ro", markersize=2, label="Starting_point")
    # plt.plot(pt_highest.x, pt_highest.y, "go", markersize=2, label="Highest_point")
    #
    # # Add a color-bar for the elevation buffer
    # cbar = fig.colorbar(ele_img, cmap='terrain', ax=ax, shrink=0.8,
    #                     norm=colors.Normalize(vmin=np.nanmin(elevation_image), vmax=np.nanmax(elevation_image)))
    #
    # # Add a North Arrow
    # arrow_x, arrow_y, arrow_length = 0.05, 0.95, 0.1
    # ax.annotate('N', xy=(arrow_x, arrow_y), xytext=(arrow_x, arrow_y - arrow_length),
    #             arrowprops=dict(facecolor='black', width=1, headwidth=3),
    #             ha='center', va='center', fontsize=5,
    #             xycoords=ax.transAxes)
    #
    # # Add a legend
    # # handles, labels = plt.gca().get_legend_handles_labels()
    # # by_label = OrderedDict(zip(labels, handles))
    # # plt.legend(by_label.values(), by_label.keys())
    # plt.legend(loc='upper right', fontsize=4)
    #
    # # Add a scale bar
    # fontprops = fm.FontProperties(size=5)
    # scalebar = AnchoredSizeBar(ax.transData,
    #                            2000, '2km', 3,
    #                            pad=0.1,
    #                            color='Black',
    #                            frameon=False,
    #                            size_vertical=1,
    #                            fontproperties=fontprops)
    #
    # ax.add_artist(scalebar)
    #
    # # Show the result map
    # plt.show()

    # plotter = Plotter(pt_user, pt_highest, g_map, path, background, iow_itn)
    # plotter.visual_path()



    # Task 6: Extend the Region


if __name__ == "__main__":
    main()
