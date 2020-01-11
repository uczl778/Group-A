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

matplotlib.use('TkAgg')


class Plotter:

    def __init__(self, pt_user, pt_highest, background):
        self.__pt_user = pt_user
        self.__pt_highest = pt_highest
        # self.__route = route
        self.__background = background

    def get_pt_user(self):
        return self.__pt_user

    def get_pt_highest(self):
        return self.__pt_highest

    # def get_route(self):
    #     return self.__route

    def get_background(self):
        return self.__background

    def plotting(self):
        pt_user = self.get_pt_user()
        pt_highest = self.get_pt_highest()
        # route = self.get_route()
        background = self.get_background()

        plt.figure()

        # Plot the background
        # row_ptu, col_ptu = background.index(pt_user.x, pt_user.y)
        # rows = row_ptu - 2000
        # cols = col_ptu - 2000
        # win = Window(cols, rows, 4000, 4000)
        # win_transform = background.window_transform(win)
        # w = background.read(1, window=win)
        # r_c_list = range(0, w.shape[1])
        # xs, ys = rasterio.transform.xy(win_transform, r_c_list, r_c_list)
        # show(w, transform=background.transform)

        background_array = background.read(1)
        palette = np.array([value for key, value in background.colormap(1).items()])
        background_image = palette[background_array]

        bounds = background_image.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]

        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1,1,1)

        # display_extent = [bounds.left + 200, bounds.right - 200, bounds.bottom + 600, bounds.top - 600]

        ax.imshow(background_image, origin="upper", extent=extent, zorder=0)

        # ax.set_extent(display_extent, crs=ccrs.OSGB())

        # Plot the starting point and the highest point
        plt.plot(pt_user.x, pt_user.y, "ro", label="Starting_point")
        plt.plot(pt_highest.x, pt_highest.y, "go", label="Highest_point")

        # Plot the legend
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.show()
