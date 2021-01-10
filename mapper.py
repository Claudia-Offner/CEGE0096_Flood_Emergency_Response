# This file is where mapping and plotting code will be developed

# Import packages here
import os
import rasterio
from rasterio.plot import show
import rasterio.crs
import rasterio.transform
from cartopy import crs
import numpy as np
import matplotlib.pyplot as plt


class Mapper:
    """ Mapper Class """

    def __init__(self, map):
        self.map = map

    def get_base(self):
        """ Loads basemap """
        background = rasterio.open(os.path.join(self.map))
        return background

    def plot_map(self, elev_mask, mask_transform, user_x, user_y, highest_x,
                 highest_y, start_x, start_y, end_x, end_y, path):
        """ Plots map features """
        ### Needs more comments #####

        background = self.get_base()
        back_array = background.read(1)
        palette = np.array([value for key, value in background.colormap(1).items()])
        background_image = palette[back_array]
        bounds = background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        display_extent = [bounds.left + 200, bounds.right - 200, bounds.bottom + 600, bounds.top - 600]

        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=crs.OSGB())  ####
        ax.imshow(background_image, origin='upper', extent=extent, zorder=0)
        # ax.set_extent(display_extent, crs=crs.OSGB()) #### Controls map zoom somehow

        # Add Points and Lines
        plt.plot(user_x, user_y, 'bo', markersize=2, label='user location')  # user location
        plt.plot(highest_x, highest_y, 'go', markersize=2, label='highest point')  # highest point location
        plt.plot(start_x, start_y, 'b+', markersize=3, label='starting point')  # starting node
        plt.plot(end_x, end_y, 'g+', markersize=3, label='ending point')  # ending node
        path.plot(ax=ax, edgecolor='blue', linewidth=0.5, zorder=2)

        # Add features
        plt.title('Flood Emergency Planning Map', fontsize=8)
        plt.legend(loc='best', fontsize=4, bbox_to_anchor=(0.5, -0.02), ncol=2)
        plt.axis('off')

        # Add raster mask
        # Set cmap
        mycmap = plt.get_cmap('viridis')
        # Values under clim will be set to totally transparent
        mycmap.set_under('k', alpha=0)
        rasterio.plot.show(elev_mask, transform=mask_transform, alpha=0.5, cmap=mycmap, clim=0)  ### Remove mask edges somehow


