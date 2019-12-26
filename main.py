from geo_classes import *
import sys


def main():
    # Task1: User Input
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
    point_user = Point("user", x, y)

    # Test whether the user is within the box
    min_x = 430000
    max_x = 465000
    min_y = 80000
    max_y = 95000
    if point_user.get_x() > max_x or point_user.get_x() < min_x or point_user.get_y() > max_y or point_user.get_y() < min_y:
        print("The user is outside this box. ")
        sys.exit()

    # Task2: Highest Point Identification

    # Task 3: Nearest Integrated Transport Network

    # Task 4: Shortest Path

    # Task 5: Map Plotting

    # Task 6: Extend the Region


if __name__ == "__main__":
    main()
