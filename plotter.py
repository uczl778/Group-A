from collections import OrderedDict

import matplotlib
import matplotlib.pyplot as plt
from rasterio import plot
import numpy as np
import cartopy.crs as ccrs
from shapely.geometry import *
from rasterio.mask import mask

matplotlib.use('TkAgg')


class Plotter:

    def __init__(self, pt_user, pt_highest, back_image,back_transform):
        self.__pt_user = pt_user
        self.__pt_highest = pt_highest
        # self.__route = route
        self.__back_image = back_image
        self.__back_transform = back_transform

    def get_pt_user(self):
        return self.__pt_user

    def get_pt_highest(self):
        return self.__pt_highest

    # def get_route(self):
    #     return self.__route

    def get_back_image(self):
        return self.__back_image

    def get_back_transform(self):
        return self.__back_transform

    def plotting(self):
        pt_user = self.get_pt_user()
        pt_highest = self.get_pt_highest()
        # route = self.get_route()
        back_image = self.get_back_image()
        back_transform = self.get_back_transform()

        # fig = plt.figure(dpi=300)
        plt.figure()

        # Plot the background
        # ax = fig.add_subplot(1,1,1, back_transform)
        
        plt.imshow(back_image)
        # palette = np.array([value for key, value in background.colormap(1).items()])
        # background_image = palette[buffered_array]
        # bounds = background_image.bounds
        # extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        # display_extent = [bounds.left + 200, bounds.right - 200, bounds.bottom + 600, bounds.top - 600]
        #

        # ax.imshow(background_image, origin="upper", extent=extent, zorder=0)
        # ax.set_extent(display_extent, crs=ccrs.OSGB())

        # Plot the starting point and the highest point
        plt.plot(pt_user.x, pt_user.y, "ro", label="Starting_point")
        plt.plot(pt_highest.x, pt_highest.y, "go", label="Highest_point")

        # Plot the legend
        handles, labels = plt.gca().get_legend_handles_labels()
        by_label = OrderedDict(zip(labels, handles))
        plt.legend(by_label.values(), by_label.keys())
        plt.show()
