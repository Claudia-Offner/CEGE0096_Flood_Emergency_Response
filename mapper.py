# This file is where mapping and plotting code will be developed
# Based on:
# https://github.com/aldolipani/CEGE0096/blob/master/5%20-%20Week/5%20-%20Drawing%20with%20Python%20with%20Solutions.ipynb
# by Aldo Lipani, date of access 07/01/2021

# Import packages here
import os
import rasterio
import rasterio.crs
import rasterio.transform
from cartopy import crs
import numpy as np
import matplotlib.pyplot as plt


class Mapper:

    def __init__(self):
        plt.figure()


    def get_map(file_path):

        background = rasterio.open(os.path.join(file_path))
        # loc_buff = location.buffer(8000)
        back_array = background.read(1)
        palette = np.array([value for key, value in background.colormap(1).items()])
        background_image = palette[back_array]
        bounds = background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        display_extent = [bounds.left+200, bounds.right-200, bounds.bottom+600, bounds.top-600]
        fig = plt.figure(figsize=(3,3), dpi=300)
        ax = fig.add_subplot(1,1,1, projection=crs.OSGB())
        ax.imshow(background_image, origin='upper', extent=extent, zorder=0)
        ax.set_extent(display_extent, crs=crs.OSGB())

    def get_features(user_x, user_y, highest_x, highest_y, start_x, start_y, end_x, end_y):

        # Plot information
        plt.plot(user_x, user_y, 'bo', markersize=2, label='user location')  # user location
        plt.plot(highest_x, highest_y, 'go', markersize=2, label='highest point')  # highest point location
        plt.plot(start_x, start_y, 'b+', markersize=3, label='starting point')  # starting node
        plt.plot(end_x, end_y, 'g+', markersize=3, label='ending point')  # ending node
        # final_path.plot(ax=ax, edgecolor='blue', linewidth=0.5, zorder=2, label='nais_path')  # path line

        # Add map features
        plt.title('Flood Emergency Planning Map', fontsize=8)
        plt.legend(loc='best', fontsize=4, bbox_to_anchor=(0.5, -0.02), ncol=2)
        plt.axis('off')
        rasterio.plot.show(elev_mask, transform=mask_transform, alpha=0.5)

        # fig = plt.figure(figsize=(3,3), dpi=300)
        # ax.imshow(background_image, origin="upper", extent=extent, zorder=0)
        # img = ax.imshow(user_image, origin="upper", extent=u_extent, alpha=0.6, zorder=1, vmin=0, cmap='terrain')
        # cx = fig.add_axes([0.91, 0.2, 0.02, 0.6])
        # cb = plt.colorbar(img, cax=cx)
        # cb.ax.tick_params(labelsize=3)


# nais_path = get_path(g, path, 'itn/solent_itn.json')
get_map('background/raster-50k_2724246.tif')
get_features(test_location.x, test_location.y, high_p.x, high_p.y, start_point.x, start_point.y, end_point.x, end_point.y)
plt.show()
