# -*- coding: utf-8 -*-
import os

import matplotlib
import matplotlib.patches as mpatches
import matplotlib.pyplot as plt

from util.util_data import date_format_d_m_Y

matplotlib.use('Agg')


def fetch_plot_graph_image(
        x_axis_data,
        y_axis_data,
        graph_folder,
        graph_path,
        label,
        scale='-'):
    try:
        plt.xlabel('Current date is {}'.format(
            x_axis_data[-1].strftime(date_format_d_m_Y)))
        plt.plot(x_axis_data, y_axis_data, scale)
        patch = mpatches.Patch(label=label)
        plt.legend(handles=[patch])
        plt.gcf().autofmt_xdate(rotation=20)
        plt.grid('minor')
        if not os.path.exists(graph_folder):
            os.makedirs(graph_folder)
        plt.savefig(graph_path)
    finally:
        plt.close()
