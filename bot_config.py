import os

browser = 'firefox'

currency_api_url = "http://www.nbrb.by/API/ExRates/Rates/Dynamics"
currency_dollar_id = '145'
currency_euro_id = '292'
currency_rur_id = '298'
currency_graph_days = 300
currency_graph_folder = os.path.join("features", "currency", "graphs")
currency_graph_path = os.path.join(currency_graph_folder, "graph.png")
currency_graph = "currency_graph"
currency_symbpls = ['$', '€', 'RUR']
currency_ids = [currency_dollar_id, currency_euro_id, currency_rur_id]
buttons_currency_selection = dict(zip(currency_ids, currency_symbpls))
button_currency_graph = {currency_graph: 'Currency Graph'}

cinema_url = "https://afisha.tut.by"
cinema_url_path_today = "/film"
cinema_url_path_soon = "/movie-premiere"
cinema_soon = "cinema_soon"
cinema_soon_params = {'utm_source': cinema_url, 'utm_medium': 'films', 'utm_campaign': 'premiere_block'}
button_cinema_soon = {cinema_soon: 'Upcoming New Movies'}

football_url = "https://matchtv.ru/football"
football_ucl_path = "/ucl"
football_le_path = "/le"
football_url_path_calendar = "/stats/calendar"
football_leagues = ['UEFA Champions League', 'UEFA Europa League']
football_leagues_cmd = [football_ucl_path, football_le_path]
buttons_football_leagues = dict(zip(football_leagues_cmd, football_leagues))

instagram_link_regexp = "https?:\/\/www\.instagram\.com\/p\/[a-zA-Z0-9\.\&\/\?\:@\-_=#]*$"
instagram_url_media_name_regexp = "[^\/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))"
instagram_post_content_folder = os.path.join("features", "instagram", "post_content")
instagram_image_type = "GraphImage"
instagram_side_type = "GraphSidecar"
instagram_video_type = "GraphVideo"

location_url = "https://yandex.by/maps/157/minsk/search/{item}/?l=sat%2Cskl&ll={longitude}%2C{latitude}&sll={longitude}%2C{latitude}&sspn=0.01%2C0.004&z=16"
location_atm = "Банкомат"
location_folder = os.path.join("features", "location", "map")