# File for developing OOP that will read analysis inputs

# Import packages here
import os
import json
import numpy as np
import geopandas as gpd
import rasterio
import rasterio.crs
import rasterio.transform
from rasterio.mask import mask
from pyproj import CRS
from shapely.geometry import Point, Polygon, MultiPolygon, LineString


def gdf_to_json(gdf):
    """ Parses a GeoDataFrame to JSON format """
    return [json.loads(gdf.to_json())['features'][0]['geometry']]


class Reader:
    """ Reader Class """

    def __init__(self, boundary):
        self.boundary = boundary

    def get_boundary(self):
        """ Retrieves Geometry from a shape file and outputs a list """

        path = self.boundary
        file = gpd.read_file(path)
        l1 = []
        for i in file['geometry']:
            for shape in i:
                l1.append(shape)
        return l1

    def get_input(self):
        """ Retrieves user inputs and outputs a Point """

        while True:
            try:
                # Set bounding box
                x = float(input('x coordinate: '))
                y = float(input('y coordinate: '))
                location = Point(x, y)
                el_mbr = Polygon([(430000, 80000.0), (465000.0, 80000.0), (465000.0, 95000.0), (430000, 95000.0)])

                # Check if user is in range
                mbr_res = el_mbr.contains(location)
                if mbr_res is True:
                    # Check if user is on the island
                    boundary = self.get_boundary()
                    res = []
                    for i in boundary:
                        res.append(i.contains(location))
                    if not any(res):
                        print('User is not on the island')
                    else:
                        return Point(x, y)
                else:
                    print('User out of range')
                    return Reader.get_input(self)

            except ValueError:
                print('Invalid data type')
                return Reader.get_input(self)

    def get_mask(self, location, data):
        """ Retrieves raster data around user input; outputs as a 5km mask """

        crs = CRS.from_epsg(27700)  # set CRS to BNS
        buff = location.buffer(5000)  # create 5km radius buffer

        # Extract info from buffer into dataframe and coordinates
        buff_gdf = gpd.GeoDataFrame({'geometry': buff}, index=[0], crs=crs)
        buff_coords = gdf_to_json(buff_gdf)

        # Extract raster values with mask, with no data set to -10
        with rasterio.open(data) as elev:
            elev_mask, mask_transform = rasterio.mask.mask(elev, shapes=buff_coords, crop=True, nodata=-1)

        return [elev_mask, mask_transform]  # returns as an array

    def get_raster(self, elevation, mask, trans):

        # Load meta data
        meta_data = elevation.meta.copy()
        meta_data.update(
            {"driver": "GTiff", "height": mask.shape[1], "width": mask.shape[2],
                "transform": trans,
                "crs": CRS.from_epsg(27700).to_proj4()})

        # Write file
        with rasterio.open('output.tif', 'w', **meta_data) as dest:
            dest.write(mask)
