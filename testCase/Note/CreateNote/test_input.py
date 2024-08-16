import time
import unittest
from copy import deepcopy

from parameterized import parameterized

from business.dataClear import DataClear
from common.logsMethod import info, class_case_log, step
from common.checkOutput import CheckOutput
from business.apiRe import post
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator


@class_case_log
class CreateNoteInput(unittest.TestCase):
    envConfig = YamlRead().env_config()
    dataConfig = YamlRead().data_config()['CreateNoteInput']
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    mustKeys = dataConfig['mustKeys']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    body_content_base = {"noteId": DataGenerator.generate_time_str() + "_noteId",
                         "title": DataGenerator.generate_str_title(),
                         "summary": DataGenerator.generate_str_summary(), "body": DataGenerator.generate_str_body(),
                         "localContentVersion": 1, "BodyType": 0}

    def setUp(self):
        DataClear().note_clear()

    def tearDown(self):
        DataClear().note_clear()

    @parameterized.expand(mustKeys)
    def testCase01_createNoteFailed(self, key):
        """新建便签内容，必填项缺失"""
        info(f"必填项{key}缺失")
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content.pop(key)
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase02_createNoteFailed(self):
        """新建便签内容，必填项noteId为整数校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_int()}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase03_createNoteFailed(self):
        """新建便签内容，必填项noteId为特殊字符校验"""
        step("前置构建便签主体")
        body_main = {"noteId": "%4￥#@&……"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase04_createNoteFailed(self):
        """新建便签内容，必填项noteId为None校验"""
        step("前置构建便签主体")
        body_main = {"noteId": None}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase05_createNoteSuccess(self):
        """新建便签内容，必填项noteId为中文校验"""
        step("前置构建便签主体")
        body_main = {"noteId": "测试中文"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase06_createNoteFailed(self):
        """新建便签内容，必填项title为整数校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["title"] = int(time.time() * 1000)
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase07_createNoteFailed(self):
        """新建便签内容，必填项title为特殊字符校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["title"] = "%4￥#@&……"
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase08_createNoteFailed(self):
        """新建便签内容，必填项title为None校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["title"] = None
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase09_createNoteSuccess(self):
        """新建便签内容，必填项title为中文校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["title"] = "测试标题"
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase10_createNoteFailed(self):
        """新建便签内容，必填项summary为整数校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["summary"] = int(time.time() * 1000)
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase11_createNoteFailed(self):
        """新建便签内容，必填项summary为特殊字符校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["summary"] = "%4￥#@&……"
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase12_createNoteFailed(self):
        """新建便签内容，必填项summary为None校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["summary"] = None
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase13_createNoteSuccess(self):
        """新建便签内容，必填项summary为中文校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["summary"] = "测试摘要"
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase14_createNoteFailed(self):
        """新建便签内容，必填项body为整数校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["body"] = int(time.time() * 1000)
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase15_createNoteFailed(self):
        """新建便签内容，必填项body为特殊字符校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["body"] = "%4￥#@&……"
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(500, res.status_code)
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase16_createNoteFailed(self):
        """新建便签内容，必填项body为None校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["body"] = None
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase17_createNoteSuccess(self):
        """新建便签内容，必填项body为中文校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["body"] = "测试正文内容"
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase18_createNoteFailed(self):
        """新建便签内容，必填项localContentVersion为字符串校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["localContentVersion"] = "0"
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase19_createNoteSuccess(self):
        """新建便签内容，必填项localContentVersion为整数校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["localContentVersion"] = 0
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"responseTime": int, "contentVersion": 1, "contentUpdateTime": int}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase20_createNoteFailed(self):
        """新建便签内容，必填项localContentVersion为浮点数校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["localContentVersion"] = 0.0
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据

    def testCase21_createNoteFailed(self):
        """新建便签内容，必填项localContentVersion为None校验"""
        step("前置构建便签主体")
        body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
        post(url=self.host + "/v3/notesvr/set/noteinfo", headers=self.headers, data=body_main, sid=self.sid1)
        step(f"构建便签主体，noteId:{body_main['noteId']}")
        step(f"新建便签内容")
        body_content = deepcopy(self.body_content_base)
        body_content["noteId"] = body_main["noteId"]
        body_content["localContentVersion"] = None
        res = post(url=self.host + "/v3/notesvr/set/notecontent", headers=self.headers, data=body_content,
                   sid=self.sid1)
        self.assertEqual(200, res.status_code)
        expect = {"errorCode": -7, "errorMsg": "参数不合法！"}
        CheckOutput().output_check(expect=expect, actual=res.json())
        # 获取首页便签，断言是否存在新增的便签数据
