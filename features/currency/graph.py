# -*- coding: utf-8 -*-
import os

import matplotlib.pyplot as plt

from config import currency_graph_path


def fetch_currency_graph(currency_data):
    x = [currency_day.Date for currency_day in currency_data]
    y = [currency_day.Cur_OfficialRate for currency_day in currency_data]

    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    plt.savefig(currency_graph_path)
    plt.close()
