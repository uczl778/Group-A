from shapely.geometry import *
from pyproj import *
import rasterio
import sys
from highest_pt import *


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
    point_user = Point(x, y)

    # Test whether the user is within the box
    min_x = 430000
    max_x = 465000
    min_y = 80000
    max_y = 95000
    if point_user.x > max_x or point_user.x < min_x or point_user.y > max_y or point_user.y < min_y:
        print("The user is outside this box. ")
        sys.exit()

    # Task2: Highest Point Identification
    ele_fp = 'F:/PycharmProjects/Material/elevation/SZ.asc'
    # ele_fp = sys.argv[3]
    elevation = rasterio.open(ele_fp)
    point_high = highest_pt(point_user, elevation)
    pt_high, max_ele = point_high.get_highest_pt()

    print("The coordinate of the highest point is: " + str(pt_high.x) + ", "+ str(pt_high.y))
    print("The elevation of the highest point is: " + str(max_ele))

    # Task 3: Nearest Integrated Transport Network

    # Task 4: Shortest Path

    # Task 5: Map Plotting

    # Task 6: Extend the Region


if __name__ == "__main__":
    main()
