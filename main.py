# -*- coding: utf-8 -*-

import random
import sys
import time
from queue import Queue

from korail2 import *

KORAIL_ID = ''
KORAIL_PW = ''

PUSHOVER_APP_TOKEN = 'APP_TOKEN'
PUSHOVER_USER_TOKEN = 'USER_TOKEN'


class Request:
    def __init__(self, dep, arv, dep_date, dep_time, psgrs, train_type):
        self.dep = dep
        self.arv = arv
        self.dep_date = dep_date
        self.dep_time = dep_time
        self.psgrs = psgrs
        self.train_type = train_type


def sendnoti(msg):
    pass


def main(request):
    queue_req = Queue()
    [queue_req.put(r) for r in request]

    k = Korail(KORAIL_ID, KORAIL_PW, auto_login=False)
    if not k.login():
        print("login fail")
        exit(-1)

    while not queue_req.empty():
        time.sleep(random.uniform(3.0, 5.1))
        req = queue_req.get()
        Found = False
        try:
            sys.stdout.write("Finding Seat %s ➜ %s \n" % (req.dep, req.arv))
            trains = k.search_train_allday(
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
            print(e)
            queue_req.put(req)

        if Found:
            k.login()
            try:
                sys.stdout.write("Trying to reserve : ")
                seat = k.reserve(trains[0], passengers=req.psgrs)
                print(" → Reserved : {}".format(seat))
                sendnoti(repr(seat))
            except KorailError as e:
                print(" → Failed : {}".format(e))
                queue_req.put(req)
                sendnoti(e)
        print("")


if __name__ == "__main__":
    main(
        request=[
            Request('수원', '동대구', '20220209', '080000', [AdultPassenger(1)], TrainType.KTX),
            Request('동대구', '수원', '20220207', '080000', [AdultPassenger(1)], TrainType.KTX),
        ]
    )
