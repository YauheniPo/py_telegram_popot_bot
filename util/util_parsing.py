# -*- coding: utf-8 -*-

from lxml import html


def get_items(site_content, items_xpath):
    tree_html_content = html.fromstring(site_content)
    return tree_html_content.xpath(items_xpath)
