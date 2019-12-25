import os

import matplotlib.pyplot as plt


def fetch_currency_graph(currency_data):
    x = [currency_day.Date for currency_day in currency_data]
    y = [currency_day.Cur_OfficialRate for currency_day in currency_data]

    plt.plot(x, y)
    plt.gcf().autofmt_xdate()
    if not os.path.exists('graphs'):
        os.makedirs('graphs')
    plt.savefig(os.path.join("graphs", "graph.png"))
    plt.close()
