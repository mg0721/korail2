import random
import sys
import time
from queue import Queue
from typing import List

from korail2 import Korail, NoResultsError, KorailError
from runner.request import Request


class KorailRunner:
    def __init__(self, id: str, pwd: str):
        self.k = Korail(id, pwd, auto_login=False)
        if not self.k.login():
            print("login fail")
            sys.exit()

        self.queue_req: Queue = Queue()

    def sendnoti(self, msg):
        pass

    def run(self, requests: List[Request], num: int):
        [self.queue_req.put(r) for r in requests]

        while not self.queue_req.empty():
            time.sleep(random.uniform(3.0, 5.1))
            req = self.queue_req.get()
            trains = []
            try:
                sys.stdout.write("Finding Seat %s ➜ %s \n" % (req.dep, req.arv))
                trains += self.k.search_train_allday(
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
            except NoResultsError:
                sys.stdout.write("No Seats \n")
                self.queue_req.put(req)
            except Exception as e:
                print(f'{type(e).__name__}: {e}')
                self.queue_req.put(req)

            success = False
            if trains:
                self.k.login()
                for idx, t in enumerate(trains):
                    if idx > num - 1:
                        break
                    try:
                        sys.stdout.write("Trying to reserve : ")
                        seat = self.k.reserve(t, passengers=req.psgrs, option=req.seat_type)
                        print(" → Reserved : {}".format(seat))
                        self.sendnoti(repr(seat))
                        success = True
                        break
                    except KorailError as e:
                        print(f" → Failed({idx}): {t} > {e}")
                        self.sendnoti(e)
            if not success:
                self.queue_req.put(req)
            print("")
