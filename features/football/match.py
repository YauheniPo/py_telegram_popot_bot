# -*- coding: utf-8 -*-


class Match:

    def __init__(self, host_team: str, guest_team: str, date: str):
        if not host_team:
            host_team = [""]
        if not guest_team:
            guest_team = [""]
        self.host_team = host_team[0]
        self.guest_team = guest_team[0]
        self.date = str(date[0]).strip()
