# -*- coding: utf-8 -*-
import datetime
from dataclasses import dataclass

from util.util_data import DATE_FORMAT_ISO


@dataclass
class Currency:
    Cur_ID: int
    Cur_OfficialRate: float

    def __init__(self, Cur_ID, Date, Cur_OfficialRate):
        self.Cur_ID = Cur_ID
        self.Date = datetime.datetime.strptime(Date, DATE_FORMAT_ISO)
        self.Cur_OfficialRate = Cur_OfficialRate
