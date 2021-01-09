# This is where Assignment 2 will be developed to solve tasks.

# Import the necessary modules here
from reader import
from itn import
from mapper import

# Import necessary packages here
# import json
# import geopandas as gpd
# import rasterio
# import rasterio.crs
# import rasterio.transform
# from pyproj import CRS
# from shapely.geometry import Point, Polygon, MultiPolygon, LineString
# from shapely.geometry import Point
# import os
# import fiona
# import pandas as pd
# import numpy as np
# import matplotlib.pyplot as plt
# from rasterio import plot
# from rasterio.plot import show
# from rasterio.mask import mask
# from rasterio.windows import from_bounds
# import networkx as nx
# from rtree import index

# Add extra functions here


def main():
    """ Flood Emergency Planning """

    # TASK 1: USER INPUT
    # isle_bound = shp_to_list('shape/isle_of_wight.shp')
    # location = user_input(isle_bound)
    # print(location)
    test_location = Point(450000, 85000)
    print('user: ', test_location)

    # TASK 2: HIGHEST POINT IDENTIFICATION

    elev_mask, mask_transformation = data_buffer(test_location, 'raster', 'elevation\SZ.asc')
    highest_point_value = np.max(elev_mask)
    highest_point_place = np.where(elev_mask[0] == highest_point_value)
    highest_point = Point(test_location.x - 5002.5 + highest_point_place[1][0] * 5,
                          test_location.y + 5002.5 - highest_point_place[0][0] * 5)
    highest_p = highest_point.xy
    x2 = highest_point.x
    y2 = highest_point.y
    print('Highest point in 5km radius: ', (x2, y2))
    high_p = Point(445022.5, 85517.5)
    print('highest point: ', high_p)

    # TASK 3: NEAREST ITN

    itn_nodes = get_json('itn/solent_itn.json')
    start_node = nearest_node(test_location, itn_nodes)
    end_node = nearest_node(high_p, itn_nodes)
    print('Start Location:', start_node, 'End Location:', end_node)
    start_point = Point(start_node[1][0], start_node[1][1])
    end_point = Point(end_node[1][0], end_node[1][1])

    # TASK 4: SHORTEST PATH

    itn_links = get_json('itn/solent_itn.json')['roadlinks']
    elevation = rasterio.open('elevation/SZ.asc')
    shortest = shortest_path(start_node[0], end_node[0], itn_links)
    print('Dijkstra Path: ', shortest)
    nais = naismiths_path(itn_links, elevation, start_node[0], end_node[0])
    print('Naismiths Path: ', nais)

    # Task 5: Map Plotting

    get_map('background/raster-50k_2724246.tif')
    get_features(test_location.x, test_location.y, high_p.x, high_p.y, start_point.x, start_point.y, end_point.x,
                 end_point.y)
    plt.show()

    # Task 6: Extend the Region


if __name__ == '__main__':
    main()