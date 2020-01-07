# -*- coding: utf-8 -*-
import json
import logging
import re

import requests

from config import *
from features.instagram.insta_post import InstaPost
from util.util_parsing import get_tree_html_content, json_data_regex

logger = logging.getLogger(__name__)


def get_insta_post_data(post_content):
    # --side
    # entry_data
    # PostPage
    # graphql
    # shortcode_media
    # edge_sidecar_to_children and "__typename": "GraphSidecar", and edge_media_to_caption
    # edges
    # [node]
    # [display_url]

    insta_post_data_script_xpath = "//script[@type='text/javascript'][contains(text(),'window._sharedData = {')]//text()"
    insta_post_data_script_content = re.search(
        json_data_regex, get_tree_html_content(post_content).xpath(insta_post_data_script_xpath)[0]).group(0)

    insta_post_data_json = json.loads(insta_post_data_script_content)
    insta_post_media_content_json = insta_post_data_json['entry_data']['PostPage'][0]['graphql']['shortcode_media']

    insta_post = InstaPost(content_type=insta_post_media_content_json['__typename'])
    if insta_post.content_type == instagram_side_type:
        None
    elif insta_post.content_type == instagram_image_type:
        insta_post_description = insta_post_media_content_json['edge_media_to_caption']['edges']
        insta_post.set_description(insta_post_description)
        insta_post_media_url = insta_post_media_content_json['display_url']
        insta_post.append_media_url(insta_post_media_url)
    elif insta_post.content_type == instagram_video_type:
        insta_post_description = insta_post_media_content_json['edge_media_to_caption']['edges']
        insta_post.set_description(insta_post_description)
        insta_post_media_url = insta_post_media_content_json['video_url']
        insta_post.append_media_url(insta_post_media_url)
    else:
        logger.error("Instagram post does not exist expected type for parsing: {}".format(insta_post))

    return insta_post


def fetch_insta_post_content_files(insta_post):
    for (url, path) in zip(insta_post.media_url, insta_post.media_content_path):
        requests_url = requests.get(url)
        if not os.path.exists(instagram_post_content_folder):
            os.makedirs(instagram_post_content_folder)
        with open(path, 'wb') as f:
            f.write(requests_url.content)
