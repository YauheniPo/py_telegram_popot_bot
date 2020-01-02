# -*- coding: utf-8 -*-
import json
import logging
import os

import requests

from config import instagram_image_folder
from features.instagram.insta_post import InstaPost
from util.util_parsing import get_tree_html_content

logger = logging.getLogger(__name__)


def get_insta_post_data(post_content):
    tree_html_content = get_tree_html_content(post_content)
    image_utl = tree_html_content.xpath("//meta[@property='og:image']")[0].get('content')
    tree_post_description = tree_html_content.xpath("//script[@type='application/ld+json']//text()")
    warning_msg = None
    post_description = None
    if not tree_post_description:
        warning_msg = 'This Instagram post does not a PUBLIC.'
    else:
        post_description = json.loads(str(tree_post_description[0]).strip()) \
            .get('caption', 'post without description')
    return InstaPost(image_url=image_utl, post_description=post_description, warning=warning_msg)


def fetch_insta_post_image(insta_post):
    f = None
    photo_name = insta_post.image_path
    try:
        requests_url = requests.get(insta_post.image_url)
        if not os.path.exists(instagram_image_folder):
            os.makedirs(instagram_image_folder)
        f = open(photo_name, 'ab')
        f.write(requests_url.content)
    except:
        logger.error(u"Save image ERROR: {}".format(photo_name))
        insta_post.warning = 'Save image ERROR'
    finally:
        if f is not None:
            f.close()
