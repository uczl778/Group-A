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
    # tuple_user = (450000, 83000)
    tuple_user = (sys.argv[1], sys.argv[2])
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
    ele_fp = 'F:/PycharmProjects/Material/elevation/SZ.asc'
    elevation = rasterio.open(ele_fp)
    # Create an object of the highest point
    point_highest = highest_pt(pt_user, elevation)
    pt_highest, max_ele, buffer_ele = point_highest.get_highest_pt()

    print("The coordinate of the highest point is: " + str(pt_highest.x) + ", " + str(pt_highest.y))
    print("The elevation of the highest point is: " + str(max_ele))

    # Task 3: Nearest Integrated Transport Network
    node_user_id = itn(pt_user.x, pt_user.y)
    print(node_user_id)
    node_highest_id = itn(pt_highest.x, pt_highest.y)
    print(node_highest_id)

    # Task 4: Shortest Path
    # Read the network
    iow_itn_json = "F:/PycharmProjects/Material/itn/solent_itn.json"
    with open(iow_itn_json, "r") as f:
        iow_itn = json.load(f)
    # Read the elevation info
    dataset = elevation
    # View the route, load the background map
    mersea_background = "F:/PycharmProjects/Material/background/raster-50k_2724246.tif"
    background = rasterio.open(str(mersea_background))
    # The start point and end point
    start = node_user_id
    end = node_highest_id
    # Create an object of the shortest path
    path_shortest = shortest_path(start, end, iow_itn, dataset)
    g_map = path_shortest.g_map()
    path = path_shortest.shortest_path(g_map)

    # Task 5: Map Plotting

    plotter = Plotter(pt_user, pt_highest, background, elevation, g_map, path, iow_itn)
    plotter.visual_path()

    # Task 6: Extend the Region


if __name__ == "__main__":
    main()
