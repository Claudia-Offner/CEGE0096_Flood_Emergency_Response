# This file is where Assignment 2 tasks will be solved.

# Import necessary packages here
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Add extra functions here

# Read files here
isle = gpd.read_file('shape/isle_of_wight.shp')


def main():
    """ Flood Emergency Planning """

    # TASK 1: User Input

    # Get user inputs
    print('Please input your current location as a British National Grid coordinate')
    x1 = 429900  # x1 = float(input('x coordinate: '))
    y1 = 84600  # y1 = float(input('y coordinate: '))
    # Convert inputs into Point object and elevation boundary into Polygon object
    user_p = Point(x1, y1)
    el_mbr = Polygon([(430000, 80000.0), (465000.0, 80000.0), (465000.0, 95000.0), (430000, 95000.0)])
    # Get MBR
    mbr_res = el_mbr.contains(user_p)
    print(mbr_res)
    # Task 6: Extend the region
    if not mbr_res:
        isl_poly = []
        for i in isle['geometry']:
            for poly in i:
                isl_poly.append(poly)
        print(isl_poly)
        print(len(isl_poly))
        # Check if user input is within polygons OR on border
        for i in isl_poly:
            if i.contains(user_p) or i.touches(user_p):
                mbr_res = True
                break
            else:
                mbr_res = False
                continue
    print(mbr_res)
    # if mbr_res:
    #    # Here goes everything else, they only take effect when mbr_res is True.
    # Task 2: Highest Point Identification

    # Task 3: Nearest Integrated Transport Network (ITN)

    # Task 4: Shortest Path

    # Task 5: Map Plotting


if __name__ == '__main__':
    main()