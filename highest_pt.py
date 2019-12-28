import math
import numpy as np
from rasterio.windows import Window
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

        # Create a window of user point
        x_corner = 425000
        y_corner = 75000
        radius = 5000
        pt_x = math.ceil((pt_user.x - x_corner) / 5) - radius / 5
        pt_y = math.ceil((pt_user.y - y_corner) / 5) - radius / 5
        win = elevation.read(1, window=Window(pt_x, pt_y, radius / 5 * 2, radius / 5 * 2))

        # create a circle buffer of user point
        pt_cir = Point(radius / 5, radius / 5)
        for i in range(2000):
            for j in range(2000):
                pt_temp = Point(i, j)
                dis = pt_cir.distance(pt_temp)
                if dis > 1000:
                    win[i, j] = 0

        # Identify the highest point
        max_ele = np.max(win)
        re = np.where(win == max_ele)
        re_x = re[0][0] * 5 + x_corner
        re_y = re[0][1] * 5 + y_corner

        return max_ele, re_x, re_y

        # bigWin = np.zeros((10000, 10000))
        # for i in range(10000):
        #     for j in range(10000):
        #         m = int(i / 5)
        #         n = int(j / 5)
        #         bigWin[i, j] = win[m, n]
        #
        # # create a circle buffer of user point
        # pt_cir = Point(radius, radius)
        # for i in range(10000):
        #     for j in range(10000):
        #         pt_temp = Point(i, j)
        #         dis = pt_cir.distance(pt_temp)
        #         if dis > radius:
        #             bigWin[i, j] = 0
        #
        # # Identify the highest point
        # max_ele = np.max(bigWin)
        # re = np.where(bigWin == max_ele)
        # re_x = pt_user.x - radius + re[0][0]
        # re_y = pt_user.y - radius + re[0][1]
        #
        # return max_ele, re_x, re_y
