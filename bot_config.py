import os

browser = 'chrome'

currency_api_url = "http://www.nbrb.by/API/ExRates/Rates/Dynamics"
currency_dollar_id = '145'
currency_euro_id = '292'
currency_rur_id = '298'
currency_graph_days = 300
currency_graph_folder = os.path.join("features", "currency", "graphs")
currency_graph_path = os.path.join(currency_graph_folder, "graph.png")
currency_symbols = ['$', '€', 'RUR']
currency_ids = [currency_dollar_id, currency_euro_id, currency_rur_id]
buttons_currency_selection = dict(zip(currency_ids, currency_symbols))
currency_graph = "currency_graph"
button_currency_graph = {currency_graph: 'Currency Graph'}
currency_alarm = "currency_alarm"
button_currency_alarm = {currency_alarm: 'Currency Alarm'}
buttons_currency_alarm_rate = {"- 0.1": "- 0.1", "+ 0.1": "+ 0.1"}
currency_alarm_rate_button_regexp = r"(\+|-) 0.1"
currency_alarm_rate_regexp = r"\d\.\d$"

cinema_url = "https://afisha.tut.by"
cinema_url_path_today = "/film"
cinema_url_path_soon = "/movie-premiere"
cinema_soon = "cinema_soon"
cinema_soon_params = {
    'utm_source': cinema_url,
    'utm_medium': 'films',
    'utm_campaign': 'premiere_block'}
button_cinema_soon = {cinema_soon: 'Upcoming New Movies'}

football_url = "https://matchtv.ru/football"
football_ucl_path = "/ucl"
football_le_path = "/le"
football_url_path_calendar = "/stats/calendar"
football_leagues = ['UEFA Champions League', 'UEFA Europa League']
football_leagues_cmd = [football_ucl_path, football_le_path]
buttons_football_leagues = dict(zip(football_leagues_cmd, football_leagues))

instagram_link_regexp = r"https?:\/\/www\.instagram\.com\/p\/[a-zA-Z0-9\.\&\/\?\:@\-_=#]*$"
instagram_url_media_name_regexp = r"[^\/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))"
instagram_save_content_service = "https://savefrom.net/"
instagram_post_content_folder = os.path.join(
    "features", "instagram", "post_content")

location_url = "https://yandex.by/maps/157/minsk/search/{item}/?l=sat%2Cskl&ll={longitude}%2C{latitude}&sll={longitude}%2C{latitude}&sspn=0.01%2C0.004&z=16"
location_atm = "Банкомат"
location_folder = os.path.join("features", "location", "map")

belavia_offers = 'https://vandrouki.by/tag/belavia/'

virus_covid_data_site_url = 'https://en.wikipedia.org/wiki/Template:2019%E2%80%9320_coronavirus_pandemic_data'
virus_covid_data_api_url = 'https://api.statworx.com/covid'
covid_graph_folder = "graphs"
covid_graph_path = os.path.join(covid_graph_folder, "covid.png")
