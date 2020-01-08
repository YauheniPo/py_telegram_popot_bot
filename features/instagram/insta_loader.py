# -*- coding: utf-8 -*-
import json
import logging
import re

import requests

from config import *
from features.instagram.insta_post import InstaPost
from util.util_parsing import get_tree_html_content, json_data_regex

logger = logging.getLogger(__name__)

insta_post_json_type_media_url_dict = {instagram_image_type: 'display_url',
                                       instagram_video_type: 'video_url'}


def get_insta_post_with_content_data(insta_post_media_content_json, insta_post: InstaPost):
    media_type = insta_post_media_content_json['__typename']
    insta_post.append_media_type(media_type)
    insta_post_media_url = insta_post_media_content_json[insta_post_json_type_media_url_dict.get(media_type)]
    insta_post.append_media_url(insta_post_media_url)
    return insta_post


def get_insta_post_data(post_content):
    insta_post_data_script_xpath = "//script[@type='text/javascript'][contains(text(),'window._sharedData = {')]//text()"

    insta_post_data_script_content = re.search(
        json_data_regex, get_tree_html_content(post_content).xpath(insta_post_data_script_xpath)[0]).group(0)

    insta_post_data_json = json.loads(insta_post_data_script_content)
    insta_post_media_content_json = list(list(insta_post_data_json['entry_data'].values())[0][0]['graphql'].values())[0]
    if insta_post_media_content_json.get('is_private'):
        return InstaPost(is_private_profile=True)

    insta_post = InstaPost()

    insta_post_description = insta_post_media_content_json['edge_media_to_caption']['edges']
    insta_post.set_description(insta_post_description)
    if insta_post_media_content_json['__typename'] == instagram_side_type:
        side_type_media_data_list = insta_post_media_content_json['edge_sidecar_to_children']['edges']
        for side_media_data in side_type_media_data_list:
            get_insta_post_with_content_data(side_media_data['node'], insta_post)
    else:
        get_insta_post_with_content_data(insta_post_media_content_json, insta_post)

    return insta_post


def fetch_insta_post_content_files(insta_post: InstaPost):
    for (url, path) in zip(insta_post.media_urls, insta_post.media_content_paths):
        requests_url = requests.get(url)
        if not os.path.exists(instagram_post_content_folder):
            os.makedirs(instagram_post_content_folder)
        with open(path, 'wb') as f:
            f.write(requests_url.content)
