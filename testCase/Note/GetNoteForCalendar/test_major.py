import time
import unittest
import requests
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post, get
from common.yamlRead import YamlRead
from datetime import datetime
from dateutil.relativedelta import relativedelta


@class_case_log
class GetNoteForCalendarMajor(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        DataClear().note_clear()

    def tearDown(self):
        DataClear().note_clear()

    def testCase01_GetNoteForCalendarSuccessMajor(self):
        """查看日历下便签，主流程"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("查询日历便签")
        body = {
            "remindStartTime": int((datetime.now() - relativedelta(months=1)).timestamp() * 1000),
            "remindEndTime": int(time.time() * 1000),
            "startIndex": 0,
            "rows": 50
        }
        res = post(url=self.host + '/v3/notesvr/web/getnotes/remind', sid=self.sid1, data=body, headers=self.headers)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "webNotes": [
            {"noteId": data_msg[0]['noteId'], "createTime": int, "star": 0, "remindTime": 0, "remindType": 0,
             "infoVersion": 1, "infoUpdateTime": int, "groupId": None, "title": data_msg[0]['title'],
             "summary": data_msg[0]['summary'],
             "thumbnail": None, "contentVersion": 1, "contentUpdateTime": int}]}
        CheckOutput().output_check(expect=expect, actual=res.json())
