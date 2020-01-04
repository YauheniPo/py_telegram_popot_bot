# -*- coding: utf-8 -*-
import os
import re

from config import instagram_url_image_name_regexp, instagram_image_folder


class InstaPost:

    def __init__(self, image_url, post_description=None, warning=None):
        self.image_url = image_url
        self.post_description = post_description
        self.warning = warning
        if post_description is not None:
            post_image_name = re.sub('[^0-9a-zA-Z]', '_',
                                     post_description[:100] + re.search(instagram_url_image_name_regexp, image_url)
                                     .group(0)) + ".jpg"
            self.image_path = os.path.join(instagram_image_folder, post_image_name)
