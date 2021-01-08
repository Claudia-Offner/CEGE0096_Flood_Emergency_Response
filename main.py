# This file is where Assignment 2 tasks will be solved.

# Import necessary packages here
import rasterio
from shapely.geometry import Point, Polygon
from pyproj import CRS
from rasterio.plot import show
from rasterio.mask import mask
from rasterio.windows import from_bounds
import rasterio.crs
import rasterio.transform
import geopandas as gpd
import numpy as np

# Add extra functions here
# https://automating-gis-processes.github.io/CSC18/lessons/L6/clipping-raster.html Time of access: 19/12/2020
def getfeatures(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


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
    crs = CRS.from_epsg(27700)
    location = Point(x1, y1)
    print('Creating 5km buffer around current location...')
    location_buf = location.buffer(5000)
    location_buf_gdf = gpd.GeoDataFrame({'geometry': location_buf}, index=[0], crs=crs)
    location_buf_coords = getfeatures(location_buf_gdf)
    print('Reading elevation file...')
    with rasterio.open('elevation\SZ.asc') as elev:
        elev_mask, mask_transform = rasterio.mask.mask(elev, shapes=location_buf_coords, crop=True)
    # rasterio.plot.show(elev_mask, transform=mask_transform)
    print('Searching highest point...')
    highest_point_value = np.max(elev_mask)
    highest_point_place = np.where(elev_mask[0] == highest_point_value)
    # print(elev_mask[0][highest_point_place])
    highest_point = Point(location.x - 5002.5 + highest_point_place[1][0] * 5, location.y + 5002.5 - highest_point_place[0][0] * 5)
    print("The highest point's coordinates are: " + 'x=' + str(highest_point.x) + ', ' + 'y=' + str(highest_point.y))
    
    # Task 3: Nearest Integrated Transport Network (ITN)
    #identify nearest nodes to person
    with open('itn/solent_itn.json') as f:
        data = json.load(f)
    nodes = []
    for feature in data['roadnodes']:
        nodes.append(data['roadnodes'][feature]['coords'])
    node_idx = index.Index()
    for i, node in enumerate(nodes):
        node_idx.insert(i, node, str(i))
    person_closest = []
    for i in node_idx.nearest((x1,y1), num_results=1, objects=True):
        person_closest.append(i.id)
        person_closest.append(i.bounds[0])
        person_closest.append(i.bounds[2])
    print('the closest point to user is:', person_closest)
    highest_closest = []
    for i in node_idx.nearest((highest_point.x,highest_point.y), num_results=1, objects=True):
        highest_closest.append(i.id)
        highest_closest.append(i.bounds[0])
        highest_closest.append(i.bounds[2])
    print('the closest point to highest point is:', highest_closest)
    # Task 4: Shortest Path

    # Task 5: Map Plotting

    # Task 6: Extend the Region


if __name__ == '__main__':
    main()
