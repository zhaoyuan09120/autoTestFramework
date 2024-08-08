import time
import unittest
import requests
from parameterized import parameterized

from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.logsMethod import class_case_log
from business.apiRe import post, get
from common.yamlRead import YamlRead
from datetime import datetime
from dateutil.relativedelta import relativedelta


@class_case_log
class GetNoteForCalendarInput(unittest.TestCase):
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()['GetNoteForCalendar']
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    mustKey = dataConfig['mustKeys']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        DataClear().note_clear()

    @parameterized.expand(mustKey)
    def testCase01_GetNoteForCalendarFailed(self, key):
        """查看日历下便签，必填项校验"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("查询日历便签")
        body = {
            "remindStartTime": int((datetime.now() - relativedelta(months=1)).timestamp() * 1000),
            "remindEndTime": int(time.time() * 1000),
            "startIndex": 0,
            "rows": 50
        }
        body.pop(key)
        res = post(url=self.host + '/v3/notesvr/web/getnotes/remind', sid=self.sid1, data=body, headers=self.headers)
        self.assertEqual(412, res.status_code)

    @parameterized.expand(mustKey)
    def testCase02_GetNoteForCalendarSuccess(self, key):
        """查看日历下便签，必填项数据类型str校验"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("查询日历便签")
        body = {
            "remindStartTime": int((datetime.now() - relativedelta(months=1)).timestamp() * 1000),
            "remindEndTime": int(time.time() * 1000),
            "startIndex": 0,
            "rows": 50
        }
        body[key] = str(body[key])
        res = post(url=self.host + '/v3/notesvr/web/getnotes/remind', sid=self.sid1, data=body, headers=self.headers)
        self.assertEqual(200, res.status_code)

    @parameterized.expand(mustKey)
    def testCase03_GetNoteForCalendarFailed(self, key):
        """查看日历下便签，必填项数据值为None校验"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("查询日历便签")
        body = {
            "remindStartTime": int((datetime.now() - relativedelta(months=1)).timestamp() * 1000),
            "remindEndTime": int(time.time() * 1000),
            "startIndex": 0,
            "rows": 50
        }
        body[key] = None
        res = post(url=self.host + '/v3/notesvr/web/getnotes/remind', sid=self.sid1, data=body, headers=self.headers)
        self.assertEqual(412, res.status_code)

    @parameterized.expand(mustKey)
    def testCase04_GetNoteForCalendarFailed(self, key):
        """查看日历下便签，必填项特殊字符校验"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("查询日历便签")
        body = {
            "remindStartTime": int((datetime.now() - relativedelta(months=1)).timestamp() * 1000),
            "remindEndTime": int(time.time() * 1000),
            "startIndex": 0,
            "rows": 50
        }
        body[key] = "@#￥……%%￥"
        res = post(url=self.host + '/v3/notesvr/web/getnotes/remind', sid=self.sid1, data=body, headers=self.headers)
        self.assertEqual(500, res.status_code)
