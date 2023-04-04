from typing import List

from korail2 import Passenger, TrainType, ReserveOption


class Request:
    def __init__(self, dep: str, arv: str, dep_date: str, dep_time: str, psgrs: List[Passenger],
                 train_type: TrainType, seat_type: ReserveOption):
        self.dep: str = dep
        self.arv: str = arv
        self.dep_date: str = dep_date
        self.dep_time: str = dep_time
        self.psgrs: List[Passenger] = psgrs
        self.train_type: TrainType = train_type
        self.seat_type: ReserveOption = seat_type
