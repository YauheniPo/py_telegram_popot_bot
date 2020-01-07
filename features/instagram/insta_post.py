# -*- coding: utf-8 -*-
import re

from config import *


class InstaPost:
    media_url = []
    media_content_path = []
    post_description = None

    def __init__(self, content_type=None):
        self.content_type = content_type

    def append_media_url(self, media_url):
        self.media_url.append(media_url)

        post_image_name = re.search(instagram_url_media_name_regexp, media_url).group(0)
        self.media_content_path.append(os.path.join(instagram_post_content_folder, post_image_name))

    def set_description(self, post_description):
        self.post_description = post_description
