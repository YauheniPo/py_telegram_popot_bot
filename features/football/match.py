# -*- coding: utf-8 -*-


class Match:
    host_team: str
    guest_team: str
    date: str

    def __init__(self, host_team, guest_team, date):
        self.host_team = host_team
        self.guest_team = guest_team
        self.date = date
