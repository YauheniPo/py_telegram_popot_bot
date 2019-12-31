import os

currency_api_url = "http://www.nbrb.by/API/ExRates/Rates/Dynamics/"
currency_dollar_id = 145
currency_graph_days = 300
currency_graph_path = os.path.join("graphs", "graph.png")

cinema_url = "http://kino.bycard.by"
cinema_url_path_movie = "/movie"
cinema_url_path_soon = "/soon"
cinema_item_xpath = "//div[@class='event_item']"