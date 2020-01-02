# -*- coding: utf-8 -*-
import os
import re

from config import instagram_url_image_name_regexp, instagram_image_folder


class InstaPost:

    def __init__(self, image_url, post_description):
        self.image_url = image_url
        self.post_description = post_description
        post_image_name = post_description[:100] + re.search(instagram_url_image_name_regexp, image_url).group(0)

        image_name = (lambda s: ''.join(['_' if c in [':', '"', ' ', ','] else c for c in s]))(post_image_name)
        self.image_path = os.path.join(instagram_image_folder, image_name)
