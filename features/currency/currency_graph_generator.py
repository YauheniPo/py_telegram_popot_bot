# -*- coding: utf-8 -*-
from bot_config import currency_graph_path
from util.logger import logger
from util.util_graph import fetch_plot_graph_image


def fetch_currency_graph(currency_data):
    logger().info("Fetch currency data graph")

    x_axis_date = [currency_day.Date for currency_day in currency_data]
    y_axis_rate = [
        currency_day.Cur_OfficialRate for currency_day in currency_data]

    fetch_plot_graph_image(
        x_axis_date,
        y_axis_rate,
        currency_graph_path,
        y_axis_rate[-1])
