import copy
import time
import unittest
from business.dataClear import DataClear
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log, step
from business.apiRe import post
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator


@class_case_log
class CreateNoteMajor(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    body_content_base = {"noteId": DataGenerator.generate_time_str() + "_noteId",
                         "title": DataGenerator.generate_str_title(),
                         "summary": DataGenerator.generate_str_summary(), "body": DataGenerator.generate_str_body(),
                         "localContentVersion": 1, "BodyType": 0}

    def setUp(self):
        DataClear().note_clear()

    def tearDown(self):
        DataClear().note_clear()

    def testCase01_createNoteSuccessMajor(self):
        """新建便签内容的主流程"""
        step("构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = copy.deepcopy(self.body_content_base)
        body_content['noteId'] = body_main['noteId']
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_updateNoteSuccessMajor(self):
        """更新便签内容的主流程"""
        step("构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = copy.deepcopy(self.body_content_base)
        body_content['noteId'] = body_main['noteId']
        res_content = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                           sid=self.sid1)
        body_update = copy.deepcopy(body_content)
        body_update['noteId'] = body_content['noteId']
        body_update["title"] = DataGenerator.generate_str_title()
        body_update["summary"] = DataGenerator.generate_str_summary()
        body_update["body"] = DataGenerator.generate_str_body()
        body_update["localContentVersion"] = body_content['localContentVersion']
        body_update["BodyType"] = body_content['BodyType']
        step("更新便签")
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_update, sid=self.sid1)

        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "contentVersion": res_content.json()["contentVersion"] + 1,
                  "contentUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据
