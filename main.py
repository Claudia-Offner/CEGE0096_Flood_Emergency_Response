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
import json
from rtree import index
import networkx as nx

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
    with open('Material/itn/solent_itn.json') as f:
        data = json.load(f)
    node_idx = index.Index()
    nodes = data['roadnodes']
    for i, (idx, coord) in enumerate(nodes.items()):
        x,y = coord['coords']
        point = Point(x,y)
        if location_buf.contains(point):
            node_idx.insert(i,[x,y,x,y],idx)
    start = list(node_idx.nearest((x1, y1, x1, y1), 1, objects=True))[0]
    end = list(node_idx.nearest((highest_point.x, highest_point.y, highest_point.x, highest_point.y), 1, objects=True))[0]
    person_closest = start.object
    highest_closest = end.object
    
    print('the closest point to user is:', person_closest)
    print('the closest point to highest point is:', highest_closest)
    
    # Task 4: Shortest Path
    #find shortest path between nearest person point and nearest highest point
    elevation = rasterio.open('Material/elevation/SZ.asc')
    heights = elevation.read(1)
    spd = float(5000 / 60)
    road_links = data['roadlinks']
    Graph = nx.Graph()
    for l in road_links:
        elevation_time = 0
        full_coords = road_links[l]['coords']
        point_start = Point(tuple(road_links[l]['coords'][0]))
        for p in full_coords:
            point_end = Point(tuple(p))
            start_r, start_l = elevation.index(point_start.x, point_start.y)
            end_r, end_l = elevation.index(point_end.x, point_end.y)
            d_ele = heights[int(end_r), int(end_l)] - heights[int(start_r),int(start_l)]
            if d_ele > 0:
                elevation_time = float(d_ele/10) + elevation_time
            point_start = point_end
        time = elevation_time + road_links[l]['length'] / spd
        Graph.add_edge(road_links[l]['start'],road_links[l]['end'], fid=l, weight=time)
        point_start_reversed = Point(tuple(road_links[l]['coords'][-1]))
        for p in reversed(full_coords):
            point_end = Point(tuple(p))
            start_r, start_l = elevation.index(point_start_reversed.x, point_start_reversed.y)
            end_r, end_l = elevation.index(point_end.x, point_end.y)
            d_ele = heights[int(end_r), int(end_l)] - heights[int(start_r),int(start_l)]
            if d_ele > 0:
                elevation_time = float(d_ele/10) + elevation_time
            point_start_reversed = point_end
        time = elevation_time + road_links[l]['length'] / spd
        Graph.add_edge(road_links[l]['start'],road_links[l]['end'], fid=l, weight=time)
    path = nx.dijkstra_path(Graph, person_closest, highest_closest, weight="weight")
    print(path)
    print("the shortest path between ")
    # Task 5: Map Plotting

    # Task 6: Extend the Region


if __name__ == '__main__':
    main()
