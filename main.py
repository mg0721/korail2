# -*- coding: utf-8 -*-

from korail2 import AdultPassenger, TrainType, ReserveOption
from runner.korail_runner import KorailRunner
from runner.request import Request

KORAIL_ID = ''
KORAIL_PW = ''

k_runner = KorailRunner(KORAIL_ID, KORAIL_PW)
k_runner.run(
    requests=[
        Request('수원', '부산', '20230406', '193200', [AdultPassenger(1)], TrainType.KTX,
                ReserveOption.GENERAL_ONLY),
        Request('부산', '수원', '20230407', '194900', [AdultPassenger(1)], TrainType.KTX,
                ReserveOption.GENERAL_ONLY)],
    num=1
)
