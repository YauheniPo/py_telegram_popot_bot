# -*- coding: utf-8 -*-
import os

import matplotlib
import matplotlib.pyplot as plt

matplotlib.use('Agg')


def fetch_plot_graph_image(
        x_axis_data,
        y_axis_data,
        graph_path,
        labels,
        y_labels=['rates'],
        colors=['blue'],
        scales=['-']):
    try:
        # style
        plt.style.use('seaborn-darkgrid')

        # create figure and axis objects with subplots()
        fig, ax1 = plt.subplots()

        axis = [ax1]
        axis.append(ax1.twinx()) if len(y_axis_data) > 1 else None

        for ax, y_axis, label, scale, y_label, color in zip(axis, y_axis_data, labels, scales, y_labels, colors):
            # make a plot
            ax.plot(x_axis_data, y_axis, scale, label=label)
            # set y-axis label
            ax.set_ylabel(y_label, color=color, fontsize=10)

        plt.gcf().autofmt_xdate(rotation=20)
        fig.legend(loc="upper right")
        plt.grid('minor')

        graph_folder = os.path.dirname(graph_path)
        if not os.path.exists(graph_folder):
            os.makedirs(graph_folder)
        # save the plot as a file
        fig.savefig(graph_path,
                    format='jpeg',
                    dpi=500,
                    bbox_inches='tight')
    finally:
        plt.close()
