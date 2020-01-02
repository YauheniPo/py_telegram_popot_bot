# -*- coding: utf-8 -*-
import json
import os

import requests

from config import instagram_image_folder
from features.instagram.insta_post import InstaPost
from util.util_parsing import get_tree_html_content


def get_insta_post_data(post_content):
    tree_html_content = get_tree_html_content(post_content)
    image_utl = tree_html_content.xpath("//meta[@property='og:image']")[0].get('content')
    post_description = json.loads(str(
        tree_html_content.xpath("//script[@type='application/ld+json']//text()")[0]).strip()) \
        .get('caption', 'This Instagram post does not a PUBLIC.')
    return InstaPost(image_url=image_utl, post_description=post_description)


def fetch_insta_post_image(insta_post):
    global f
    photo_name = insta_post.image_path
    try:
        requests_url = requests.get(insta_post.image_url)
        if not os.path.exists(instagram_image_folder):
            os.makedirs(instagram_image_folder)
        f = open(photo_name, 'ab')
        f.write(requests_url.content)
    finally:
        f.close()
