# File for developing OOP for mapping.

# Import packages here
import os
import rasterio
import rasterio.crs
import rasterio.transform
from cartopy import crs
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1.anchored_artists import AnchoredSizeBar
import matplotlib.font_manager as fm


class Mapper:
    """ Mapper Class """

    def __init__(self, map):
        self.map = map

    def get_base(self):
        """ Loads basemap """
        background = rasterio.open(os.path.join(self.map))
        return background

    def plot_map(self, region, user, highest, start, end, short_path, fast_path):
        """ Plots map features """

        # Load background & set colour
        background = self.get_base()
        back_array = background.read(1)
        palette = np.array([value for key, value in background.colormap(1).items()])
        background_image = palette[back_array]
        # Load raster data & set colour
        region = rasterio.open(str(region))
        user_image = region.read(1)
        user_image[user_image == -1] = np.nan
        mycmap = plt.get_cmap('terrain')  # Set cmap
        mycmap.set_under('k', alpha=0)  # Set values outside buffer to transparent

        # Set boundaries and plotting extents
        bounds = background.bounds
        extent = [bounds.left, bounds.right, bounds.bottom, bounds.top]
        u_bound = region.bounds
        u_extent = [u_bound.left, u_bound.right, u_bound.bottom, u_bound.top]

        # Add Figures
        fig = plt.figure(figsize=(3, 3), dpi=300)
        ax = fig.add_subplot(1, 1, 1, projection=crs.OSGB())
        ax.imshow(background_image, origin='upper', extent=extent, zorder=0)
        img = ax.imshow(user_image, origin='upper', extent=u_extent, alpha=0.6, zorder=1, vmin=0, cmap=mycmap)

        # Zoom to 10km
        plt.xlim([user.x - 5000, user.x + 5000])  # set x-axis extent
        plt.ylim([user.y - 5000, user.y + 5000])  # set y-axis extent

        # Plot Points and Lines
        plt.plot(user.x, user.y, 'bo', markersize=2, label='User location')  # user location Point
        plt.plot(highest.x, highest.y, 'go', markersize=2, label='Highest point')  # highest location Point
        plt.plot(start.x, start.y, 'b+', markersize=3, label='Starting point')  # starting Point
        plt.plot(end.x, end.y, 'g+', markersize=3, label='Ending point')  # ending Point
        fast_path.plot(ax=ax, edgecolor='red', linewidth=0.5, zorder=2, label='Fastest path')  # fastest path
        short_path.plot(ax=ax, edgecolor='blue', linewidth=0.5, zorder=2, label='Shortest path')  # shortest path

        # Plot features
        # Scale
        fontprops = fm.FontProperties(size=8)
        scalebar = AnchoredSizeBar(ax.transData, 2000, '2 km', 'lower left', pad=0.15, color='black',
                                   frameon=False, size_vertical=1, fontproperties=fontprops)
        ax.add_artist(scalebar)
        # North Arrow
        x, y, arrow_length = 0.1, 0.23, 0.109
        ax.annotate('N', xy=(x, y), xytext=(x, y - arrow_length),
                    arrowprops=dict(facecolor='black', width=2, headwidth=15),
                    ha='center', va='center', fontsize=8,
                    xycoords=ax.transAxes)
        plt.title('Flood Emergency Planning Map', fontsize=8)
        plt.legend(loc='best', fontsize=4, bbox_to_anchor=(0.75, -0.02), ncol=2)
        plt.axis('off')
        cx = fig.add_axes([0.91, 0.16, 0.02, 0.3])
        cb = plt.colorbar(img, cax=cx)
        cb.ax.tick_params(labelsize=4)

        return plt.show()
