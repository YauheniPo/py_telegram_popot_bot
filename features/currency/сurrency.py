# -*- coding: utf-8 -*-
import datetime
from dataclasses import dataclass

from util.util_parsing import date_format_iso


@dataclass
class Currency:
    Cur_ID: int
    Cur_OfficialRate: float

    def __init__(self, Cur_ID, Date, Cur_OfficialRate, *args, **kwargs):
        self.Cur_ID = Cur_ID
        self.Date = datetime.datetime.strptime(Date, date_format_iso)
        self.Cur_OfficialRate = Cur_OfficialRate
