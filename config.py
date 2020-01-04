import os

currency_api_url = "http://www.nbrb.by/API/ExRates/Rates/Dynamics"
currency_dollar_id = 145
currency_graph_days = 300
currency_graph_folder = os.path.join("features", "currency", "graphs")
currency_graph_path = os.path.join(currency_graph_folder, "graph.png")

uri = "https://{url}"

cinema_url = "afisha.tut.by"
cinema_url_path_today = "/film"
cinema_url_path_soon = "/movie-premiere"

football_url = "matchtv.ru/football"
football_ucl_path = "/ucl"
football_le_path = "/le"
football_url_path_calendar = "/stats/calendar"
