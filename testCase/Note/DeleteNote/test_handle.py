import time
import unittest
import requests
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post
from common.yamlRead import YamlRead
from parameterized import parameterized
from common.dataGenerator import DataGenerator


@class_case_log
class DeleteNoteInput(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        DataClear().note_clear()

    def testCase05_DeleteNoteFailed(self):
        """删除便签，noteId不存在校验"""
        step("删除便签")
        note_id = DataGenerator.generate_time_str() + "_noteId"
        body = {"noteId": note_id}
        res = post(url=self.host + '/v3/notesvr/delete', sid=self.sid1, data=body, headers=self.headers)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1002, "errorMsg": "Note Not Exist!"}
        CheckOutput().output_check(expect=expect, actual=res.json())
