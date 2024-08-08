import unittest
import requests
from business.dataClear import DataClear
from business.dataCreate import DataCreate
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post
from common.yamlRead import YamlRead


@class_case_log
class DeleteNoteMajor(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        DataClear().note_clear()

    def testCase01_DeleteNoteSuccessMajor(self):
        """删除便签，主流程"""
        step("前置构建1条便签数据")
        data_msg = DataCreate().create_note(num=1)
        step("删除便签")
        body = {"noteId": data_msg[0]['noteId']}
        res = post(url=self.host + '/v3/notesvr/delete', sid=self.sid1, data=body, headers=self.headers)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
