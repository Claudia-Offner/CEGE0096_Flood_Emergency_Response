# File for developing Assignment 2 tasks.

# Import packages here
from reader import Reader, Clipper
from itn import Networker
from mapper import Mapper
import os
import json
import rasterio
import rasterio.crs
import rasterio.transform
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
import numpy as np


def get_json(path):
    """ Function for loading JSON files """
    with open(path, "r") as f:
        itn = json.load(f)
    return itn


def main():
    """ Flood Emergency Planning """

    # TASK 1: USER INPUT
    print('Please provide your location as a British National Grid coordinate: ')
    # Extract user input as Point
    data = Reader('materials/shape/isle_of_wight.shp')
    location_p = data.get_input()
    # location_p = Point(439619, 85800)  # Test point
    print('User Location: ', location_p)



    # TASK 2: HIGHEST POINT IDENTIFICATION

    clip = Clipper(location_p, 'materials/elevation/SZ.asc')
    # Clip elevation raster to 5km buffer as an array and save to file
    elev_mask, mask_transform = clip.get_mask()

    # Extract highest point and identify coordinates
    highest_point_value = np.max(elev_mask)
    highest_point_place = np.where(elev_mask[0] == highest_point_value)

    # Convert pixel coordinates to meters (multiplying by 5 - 2.5 meters are added to account for pixel centroids)
    highest_p = Point(location_p.x - 5002.5 + highest_point_place[1][0] * 5,
                      location_p.y + 5002.5 - highest_point_place[0][0] * 5)
    print('Highest Location in 5km:  ', highest_p)



    # TASK 3: NEAREST ITN

    # Load road nodes from JSON file and set the location and highest Points
    nodes = get_json('materials/itn/solent_itn.json')['roadnodes']
    itn_nodes = Networker(location_p, highest_p, nodes)

    # Extract nodes closest to given points
    start_node, end_node = itn_nodes.nearest_nodes()
    start_p = Point(start_node[1][0], start_node[1][1])
    end_p = Point(end_node[1][0], end_node[1][1])
    print('Start and end nodes: ', start_p, end_p)



    # TASK 4: SHORTEST PATH

    # Load elevation, road links and start and end node Points
    elevation = rasterio.open('materials/elevation/SZ.asc')
    links = get_json('materials/itn/solent_itn.json')['roadlinks']
    itn_links = Networker(start_node[0], end_node[0], links)

    # Extract paths as GeoDataFrames
    shortest = itn_links.shortest_path()
    print('Shortest Path: ', shortest)
    fastest = itn_links.fastest_path(elevation)
    print('Fastest Path: ', fastest)



    # Task 5: Map Plotting

    # Extract elevation mask as TIF file for mapping
    clip.get_raster()

    # Plot extracted features to a basemap
    m = Mapper('materials/background/raster-50k_2724246.tif')
    user_region = str(os.path.join('output.tif'))
    m.plot_map(user_region, location_p, highest_p, start_p, end_p, shortest, fastest)



    # Task 6: Extend the Region
    # See reader.py

if __name__ == '__main__':
    main()