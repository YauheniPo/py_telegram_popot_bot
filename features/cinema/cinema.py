# -*- coding: utf-8 -*-


class Cinema:
    title: str
    media: str
    info: str
    ticket_link: str

    def __init__(self, title, media, info, ticket_link):
        self.title = title
        self.media = media
        self.info = info
        self.ticket_link = ticket_link
