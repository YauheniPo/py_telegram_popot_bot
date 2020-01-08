import os

uri_https = "https://{url}"

currency_api_url = "http://www.nbrb.by/API/ExRates/Rates/Dynamics"
currency_dollar_id = '145'
currency_euro_id = '292'
currency_rur_id = '298'
currency_graph_days = 300
currency_graph_folder = os.path.join("features", "currency", "graphs")
currency_graph_path = os.path.join(currency_graph_folder, "graph.png")
currency_graph = "currency_graph"
button_currency_graph = {'Currency Graph': currency_graph}
buttons_currency_selection = {'$': currency_dollar_id,
                              '€': currency_euro_id,
                              'RUR': currency_rur_id}

cinema_url = "afisha.tut.by"
cinema_url_path_today = "/film"
cinema_url_path_soon = "/movie-premiere"
cinema_soon = "cinema_soon"
cinema_soon_params = {'utm_source': cinema_url, 'utm_medium': 'films', 'utm_campaign': 'premiere_block'}
button_cinema_soon = {'Upcoming New Movies': cinema_soon}

football_url = "matchtv.ru/football"
football_ucl_path = "/ucl"
football_le_path = "/le"
football_url_path_calendar = "/stats/calendar"
buttons_football_leagues = [{'UEFA Champions League': football_ucl_path},
                            {'UEFA Europa League': football_le_path}]

instagram_link_regexp = "https?:\/\/www\.instagram\.com[a-zA-Z0-9\.\&\/\?\:@\-_=#]*$"
instagram_url_media_name_regexp = "[^\/\\&\?]+\.\w{3,4}(?=([\?&].*$|$))"
instagram_post_content_folder = os.path.join("features", "instagram", "post_content")
instagram_image_type = "GraphImage"
instagram_side_type = "GraphSidecar"
instagram_video_type = "GraphVideo"
