import copy
import time
import unittest

from business.dataClear import DataClear
from common.logsMethod import info, error, class_case_log, step
from common.checkOutput import CheckOutput
from business.apiRe import post
from common.yamlRead import YamlRead


@class_case_log
class CreateNoteHandle(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        DataClear().note_clear()

    def tearDown(self):
        DataClear().note_clear()

    def testCase01_updateNoteFailed(self):
        """更新便签内容,localContentVersion不符合要求"""
        step("构建便签主体")
        body_main = {"noteId": str(int(time.time() * 1000)) + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = {"noteId": body_main['noteId'], "title": "test", "summary": "test", "body": "test",
                "localContentVersion": 1, "BodyType": 0}
        post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content, sid=self.sid1)
        body_update = copy.deepcopy(body_content)
        body_update['noteId'] = body_content['noteId']
        body_update["title"] = "testUpdateTitle"
        body_update["summary"] = "testUpdateSummary"
        body_update["body"] = "testUpdateBody"
        body_update["localContentVersion"] = body_content['localContentVersion'] + 1
        body_update["BodyType"] = body_content['BodyType']
        step("更新便签")
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_update, sid=self.sid1)

        self.assertEqual(412, res.status_code)
        expect = {"errorCode": -1003, "errorMsg": "content version not equal!"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase02_createNoteFailed(self):
        """新建便签内容,BodyType值填写不符合要求校验"""
        step("构建便签主体")
        body_main = {"noteId": str(int(time.time() * 1000)) + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = {"noteId": body_main['noteId'], "title": "test", "summary": "test", "body": "test",
                "localContentVersion": 1, "BodyType": 2}
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content, sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据
