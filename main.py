# This file is where Assignment 2 tasks will be solved.

# Import necessary packages here
from shapely.geometry import Point, Polygon

# Add extra functions here

def main():
    """ Flood Emergency Planning """

    # TASK 1: User Input

    # Get user inputs
    print('Please input your current location as a British National Grid coordinate')
    x1 = 450000  # x1 = float(input('x coordinate: '))
    y1 = 85000  # y1 = float(input('y coordinate: '))
    # Convert inputs into Point object and elevation boundary into Polygon object
    user_p = Point(x1, y1)
    el_mbr = Polygon([(430000, 80000.0), (465000.0, 80000.0), (465000.0, 95000.0), (430000, 95000.0)])
    # Get MBR
    mbr_res = el_mbr.contains(user_p)
    print(mbr_res)

    # Task 2: Highest Point Identification

    # Task 3: Nearest Integrated Transport Network (ITN)

    # Task 4: Shortest Path

    # Task 5: Map Plotting

    # Task 6: Extend the Region

if __name__ == '__main__':
    main()