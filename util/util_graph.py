# -*- coding: utf-8 -*-
import os

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from util.util_data import DATE_FORMAT_D_M_Y

matplotlib.use('Agg')


def fetch_plot_graph_image(
        x_axis_data,
        y_axis_data,
        graph_path,
        label,
        scale='-'):
    try:
        plt.xlabel('Current date is {}'.format(
            x_axis_data[-1].strftime(DATE_FORMAT_D_M_Y)))
        plt.plot(x_axis_data, y_axis_data, scale)
        patch = mpatches.Patch(label=label)
        plt.legend(handles=[patch])
        plt.gcf().autofmt_xdate(rotation=20)
        plt.grid('minor')
        graph_folder = os.path.dirname(graph_path)
        if not os.path.exists(graph_folder):
            os.makedirs(graph_folder)
        plt.savefig(graph_path)
    finally:
        plt.close()
