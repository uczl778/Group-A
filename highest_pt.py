import numpy as np
from rasterio.mask import mask
from shapely.geometry import *


class highest_pt:

    def __init__(self, pt_user, elevation):
        self.__pt_user = pt_user
        self.__elevation = elevation

    def get_pt_user(self):
        return self.__pt_user

    def get_elevation(self):
        return self.__elevation

    def get_highest_pt(self):
        pt_user = self.get_pt_user()
        elevation = self.get_elevation()

        # Create a buffer of user point
        buffered_zone = pt_user.buffer(5000)
        dataset, win_transform = mask(elevation, [buffered_zone], crop=True, nodata=np.nan)

        # Identify the highest point
        buffer_ele = dataset[0]
        max_ele = np.nanmax(dataset[0])
        re = np.where(dataset[0] == max_ele)
        re_x, re_y = win_transform * (re[1][0], re[0][0])  # Collect the first highest point

        return Point(re_x, re_y), max_ele, buffer_ele
