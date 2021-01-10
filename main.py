# File for developing Assignment 2 tasks.

# Import the necessary modules here
from reader import Reader
from itn import Networker
from mapper import Mapper

# Import necessary packages here
import json
import rasterio
import rasterio.crs
import rasterio.transform
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
import numpy as np

# Add supporting functions here
def get_json(path):
    """ Function for loading JSON files """
    with open(path, "r") as f:
        itn = json.load(f)
    return itn

# Run main() to solve for tasks 1-6
def main():
    """ Flood Emergency Planning """

    # TASK 1: USER INPUT

    data = Reader('shape/isle_of_wight.shp')
    # location_p = data.get_input()
    # print('User Location: ', location_p)
    location_p = Point(450000, 85000)
    print('User Location: ', location_p)

    # TASK 2: HIGHEST POINT IDENTIFICATION

    elev_mask, mask_transform = data.get_buffer(location_p, 'elevation\SZ.asc')
    highest_point_value = np.max(elev_mask)
    highest_point_place = np.where(elev_mask[0] == highest_point_value)
    highest_p = Point(location_p.x - 5002.5 + highest_point_place[1][0] * 5,
                      location_p.y + 5002.5 - highest_point_place[0][0] * 5)
    print('Highest Location in 5km:  ', highest_p)

    # TASK 3: NEAREST ITN

    nodes = get_json('itn/solent_itn.json')['roadnodes']
    itn_nodes = Networker(location_p, highest_p, nodes)

    start_node, end_node = itn_nodes.nearest_nodes()
    start_p = Point(start_node[1][0], start_node[1][1])
    end_p = Point(end_node[1][0], end_node[1][1])
    print('Start and end nodes: ', start_p, end_p)

    # TASK 4: SHORTEST PATH

    elevation = rasterio.open('elevation/SZ.asc')
    links = get_json('itn/solent_itn.json')['roadlinks']
    itn_links = Networker(location_p, highest_p, links)

    dijkstra = itn_links.dijkstra_path(start_node[0], end_node[0])
    print('Dijkstra Path: ', dijkstra)

    # nais = itn_links.naismiths_path(elevation, start_node[0], end_node[0])
    # print('Naismiths Path: ', nais)

    # Task 5: Map Plotting

    m = Mapper('background/raster-50k_2724246.tif')
    m.plot_map(elev_mask, mask_transform, location_p.x, location_p.y, highest_p.x,
               highest_p.y, start_p.x, start_p.y, end_p.x, end_p.y, dijkstra)

    # Task 6: Extend the Region


if __name__ == '__main__':
    main()