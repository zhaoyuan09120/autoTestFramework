import time
import unittest

from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.logsMethod import class_case_log
from business.apiRe import post, get
from common.yamlRead import YamlRead
from datetime import datetime
from dateutil.relativedelta import relativedelta
from common.dataGenerator import DataGenerator


@class_case_log
class GetNoteForCalendarHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        DataClear().note_clear()

    def testCase01_GetNoteForCalendarFailed(self):
        """查看日历下便签，startindex超出数据范围"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("查询日历便签")
        body = {
            "remindStartTime": int((datetime.now() - relativedelta(months=1)).timestamp() * 1000),
            "remindEndTime": DataGenerator.generate_time_int(),
            "startIndex": -1,
            "rows": 50
        }
        res = post(url=self.host + '/v3/notesvr/web/getnotes/remind', sid=self.sid1, data=body, headers=self.headers)
        self.assertEqual(412, res.status_code)

    def testCase02_GetNoteForCalendarFailed(self):
        """查看日历下便签，rows超出数据行范围"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("查询日历便签")
        body = {
            "remindStartTime": int((datetime.now() - relativedelta(months=1)).timestamp() * 1000),
            "remindEndTime": DataGenerator.generate_time_int(),
            "startIndex": 0,
            "rows": -1
        }
        res = post(url=self.host + '/v3/notesvr/web/getnotes/remind', sid=self.sid1, data=body, headers=self.headers)
        self.assertEqual(412, res.status_code)
