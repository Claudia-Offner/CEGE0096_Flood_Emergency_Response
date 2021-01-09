# This is where OOP for reading data will be developed.

# Import packages here

import json
import geopandas as gpd
import rasterio
import rasterio.crs
import rasterio.transform
from pyproj import CRS
from shapely.geometry import Point, Polygon, MultiPolygon, LineString
from shapely.geometry import Point


# DATA CONVERTER PARENT CLASS

def get_json(path):
    with open(path, "r") as f:
        itn = json.load(f)
    return itn

def get_gdf(path):
    file = gpd.read_file(path)
    return file

def gdf_to_list(path):
    file = gpd.read_file(path)
    l1 = []
    for i in file['geometry']:
        for shape in i:
            l1.append(shape)
    return l1

def gdf_to_json(gdf):
    """Function to parse features from GeoDataFrame in such a manner that rasterio wants them"""
    import json
    return [json.loads(gdf.to_json())['features'][0]['geometry']]

# DATA INPUT CHILD CLASS: methodS for user_input and data_buffer

def user_input(isle_bound):

    x = float(input('x coordinate: '))
    y = float(input('y coordinate: '))
    location = Point(x, y)
    el_mbr = Polygon([(430000, 80000.0), (465000.0, 80000.0), (465000.0, 95000.0), (430000, 95000.0)])
    mbr_res = el_mbr.contains(location)

    if mbr_res == True:
        # Check if user is on the island
        res = []
        for i in isle_bound:
            res.append(i.contains(location))
        if not any(res):
            print('User is not on the island')
        else:
            return x, y
    else:
        print('User out of range')
        return user_input(isle_bound) # class

    # except ValueError:
    #     print('Invalid data type')
    #     return user_input(isle_bound)  # class


def data_buffer(location, datatype, data):

    crs = CRS.from_epsg(27700)  # set CRS to BNS
    buff = location.buffer(5000)  # create 5km radius buffer

    if datatype == 'raster':
        # Extract info from buffer into dataframe and coordinates
        buff_gdf = gpd.GeoDataFrame({'geometry': buff}, index=[0], crs=crs)
        buff_coords = gdf_to_json(buff_gdf)
        with rasterio.open(data) as elev:
            elev_mask, mask_transform = rasterio.mask.mask(elev, shapes=buff_coords, crop=True)
        return [elev_mask, mask_transform]

    elif datatype == 'json':
        return
    elif datatype == 'gpd':
        return
    else:
        return 'Invalid data type'