# -*- coding: utf-8 -*-
import re

from config import *


class InstaPost:

    def __init__(self, post_url=None):
        self.post_url = post_url
        self.is_private_profile = False
        self.post_description = None
        self.media_urls = []
        self.media_content_paths = []
        self.media_types = []

    def append_media_url(self, media_url):
        self.media_urls.append(media_url)

        post_image_name = re.search(instagram_url_media_name_regexp, media_url).group(0)
        self.media_content_paths.append(os.path.join(instagram_post_content_folder, post_image_name))

    def append_media_type(self, media_type):
        self.media_types.append(media_type)

    def set_description(self, post_description):
        self.post_description = post_description
