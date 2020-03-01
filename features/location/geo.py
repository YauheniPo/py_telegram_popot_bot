# -*- coding: utf-8 -*-
import os

from bot_config import location_folder, location_url
from logger import logger


class Geo:

    def __init__(self, latitude, longitude, search_item):
        self.latitude = latitude
        self.longitude = longitude
        self.search_item = search_item
        self.geo_map_url = location_url.format(item=search_item, longitude=longitude, latitude=latitude)
        if not os.path.exists(location_folder):
            os.makedirs(location_folder)
        self.screen_path = os.path.join(location_folder,
                                        "({})({})".format(latitude, longitude).replace('.', "_") + ".png")

        logger().info("latitude: %s; longitude: %s" % (latitude, longitude))
