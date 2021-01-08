# This file is where mapping and plotting code will be developed
# Based on:
# https://github.com/aldolipani/CEGE0096/blob/master/5%20-%20Week/5%20-%20Drawing%20with%20Python%20with%20Solutions.ipynb
# by Aldo Lipani, date of access 07/01/2021

from collections import OrderedDict
import matplotlib.pyplot as plt


class Mapper:

    def __init__(self):
        plt.figure()

    # def add_raster (i.e. background, elevation)

    # add add_vector (i.e. shape, roads, itn)
    def add_point(self, x, y, kind=None):
        if kind == 'start':
            plt.plot(x, y, 'ro', label='You are here!')
        elif kind == 'goal':
            plt.plot(x, y, 'bo', label='Your goal is there!')
    # def show

    # def close
