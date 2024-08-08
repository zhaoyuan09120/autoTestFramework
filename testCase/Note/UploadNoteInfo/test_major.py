import unittest
from business.dataClear import DataClear
from common.logsMethod import  step
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log
from business.apiRe import post
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator


@class_case_log
class UploadNoteInfoMajor(unittest.TestCase):
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()['uploadNoteInfo']
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    path = dataConfig['path']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        DataClear().note_clear()

    def testCase01_UploadNoteInfoSuccess(self):
        """上传便签主体，主流程"""
        step("上传便签主体")
        url = self.host + self.path
        body = {
            "noteId": DataGenerator.generate_time_str() + "_noteId",
            "star": 1,
            "remindTime": 1,
            "remindType": 0,
        }
        res = post(url=url, sid=self.sid1, headers=self.headers, data=body)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "infoVersion": 1, "infoUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_UpdateInfoSuccess(self):
        """更新便签主体，主流程"""
        step("更新便签主体")
        body = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        res = post(url=self.host + '/v3/notesvr/set/noteinfo', headers=self.headers, data=body, sid=self.sid1)
        infoVersion = res.json()['infoVersion']
        body = {
            "noteId": body["noteId"],
            "title": "test",
            "summary": "testUpdateSummary",
            "body": "testUpdateSummary",
            "localContentVersion": infoVersion,
            "BodyType": 0
        }
        res = post(url=self.host + '/v3/notesvr/set/noteinfo', headers=self.headers, data=body, sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "infoVersion": 2, "infoUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
