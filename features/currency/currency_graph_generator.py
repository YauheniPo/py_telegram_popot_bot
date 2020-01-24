# -*- coding: utf-8 -*-
import logging
import os

import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt

from bot_config import currency_graph_path, currency_graph_folder

logger = logging.getLogger(__name__)


def fetch_currency_graph(currency_data):
    logger.info("Fetch currency data graph")

    x = [currency_day.Date for currency_day in currency_data]
    y = [currency_day.Cur_OfficialRate for currency_day in currency_data]

    try:
        plt.plot(x, y)
        plt.gcf().autofmt_xdate()
        if not os.path.exists(currency_graph_folder):
            os.makedirs(currency_graph_folder)
        plt.savefig(currency_graph_path)
    finally:
        plt.close()
