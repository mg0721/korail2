# -*- coding: utf-8 -*-

import random
import sys
import time
from queue import Queue
from typing import List

from korail2 import *

KORAIL_ID = ''
KORAIL_PW = ''

PUSHOVER_APP_TOKEN = 'APP_TOKEN'
PUSHOVER_USER_TOKEN = 'USER_TOKEN'


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


def sendnoti(msg):
    pass


def main(requests: List[Request], num: int):
    queue_req = Queue()
    [queue_req.put(r) for r in requests]

    k = Korail(KORAIL_ID, KORAIL_PW, auto_login=False)
    if not k.login():
        print("login fail")
        exit(-1)

    while not queue_req.empty():
        time.sleep(random.uniform(3.0, 5.1))
        req = queue_req.get()
        Found = False
        trains = []
        try:
            sys.stdout.write("Finding Seat %s ➜ %s \n" % (req.dep, req.arv))
            trains += k.search_train_allday(
                req.dep,
                req.arv,
                req.dep_date,
                req.dep_time,
                passengers=req.psgrs,
                train_type=req.train_type,
                include_no_seats=True
            )
            for t in trains:
                print(" → Found : {}".format(t))
            Found = True
        except NoResultsError:
            sys.stdout.write("No Seats \n")
            queue_req.put(req)
        except Exception as e:
            print(f'{type(e).__name__}: {e}')
            queue_req.put(req)

        if Found:
            k.login()
            for idx, t in enumerate(trains):
                if idx > num - 1:
                    break
                try:
                    sys.stdout.write("Trying to reserve : ")
                    seat = k.reserve(t, passengers=req.psgrs, option=req.seat_type)
                    print(" → Reserved : {}".format(seat))
                    sendnoti(repr(seat))
                    break
                except KorailError as e:
                    print(f" → Failed({idx}): {t} > {e}")
                    queue_req.put(req)
                    sendnoti(e)
        print("")


if __name__ == "__main__":
    main(
        requests=[
            Request('서울', '동대구', '20221220', '080000',
                    [AdultPassenger(1)], TrainType.KTX, ReserveOption.GENERAL_ONLY),
            Request('동대구', '서울', '20221220', '080000',
                    [AdultPassenger(1)], TrainType.KTX, ReserveOption.GENERAL_ONLY),
        ],
        num=5
    )
