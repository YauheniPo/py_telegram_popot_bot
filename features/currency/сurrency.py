from dataclasses import dataclass
import datetime


@dataclass
class Currency:
    Cur_ID: int
    Cur_OfficialRate: float

    def __init__(self, Cur_ID, Date, Cur_OfficialRate, *args, **kwargs):
        self.Cur_ID = Cur_ID
        self.Date = datetime.datetime.strptime(Date, '%Y-%m-%dT%H:%M:%S')
        self.Cur_OfficialRate = Cur_OfficialRate
