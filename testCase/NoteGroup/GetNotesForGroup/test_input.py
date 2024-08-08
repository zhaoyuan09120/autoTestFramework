import unittest
from business.dataClear import DataClear
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log, step
from business.apiRe import post, get
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator
from business.dataCreate import DataCreate


@class_case_log
class GetNotesForGroupInput(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        """前置清理环境中的分组"""
        DataClear().note_clear()
        DataClear().group_clear()

    def tearDown(self):
        """后置清理便签和分组"""
        DataClear().note_clear()
        DataClear().group_clear()

    def testCase01_GetNotesForGroupFailed(self):
        """查看分组下标签,必填项groupId不传校验"""
        step("查看分组下的便签")
        res = post(url=self.host + '/v3/notesvr/web/getnotes/group', headers=self.headers, sid=self.sid1, data={
            "startIndex": 0,
            "rows": 20
        }, )
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1000, "errorMessage": "GroupId Requested!"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase02_GetNotesForGroupFailed(self):
        """查看分组下标签,必填项groupId传None校验"""
        step("查看分组下的便签")
        res = post(url=self.host + '/v3/notesvr/web/getnotes/group', headers=self.headers, sid=self.sid1, data={
            "groupId": None,
            "startIndex": 0,
            "rows": 20
        }, )
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMessage": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase03_GetNotesForGroupFailed(self):
        """查看分组下标签,必填项groupId传空字符串校验"""
        step("查看分组下的便签")
        res = post(url=self.host + '/v3/notesvr/web/getnotes/group', headers=self.headers, sid=self.sid1, data={
            "groupId": "",
            "startIndex": 0,
            "rows": 20
        }, )
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMessage": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase04_GetNotesForGroupFailed(self):
        """查看分组下标签,选填项startIndex传值越界校验"""
        step("前置1：创建分组")
        data_msg_group = DataCreate().create_group(order=0,num=1)
        step("前置2：在step1创建的分组下构建便签主体、内容")
        data_msg_note = DataCreate().create_note_for_group(group_id=data_msg_group[0]['groupId'], num=1)

        step("查看分组下的便签")
        res = post(url=self.host + '/v3/notesvr/web/getnotes/group', headers=self.headers, sid=self.sid1, data={
            "groupId": data_msg_group[0]["groupId"],
            "startIndex": -5,
            "rows": 20
        }, )
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMessage": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase05_GetNotesForGroupFailed(self):
        """查看分组下标签,选填项rows传值越界校验"""
        step("前置1：创建分组")
        data_msg_group = DataCreate().create_group(order=0,num=1)
        step("前置2：在step1创建的分组下构建便签主体、内容")
        data_msg_note = DataCreate().create_note_for_group(group_id=data_msg_group[0]['groupId'], num=1)

        step("查看分组下的便签")
        res = post(url=self.host + '/v3/notesvr/web/getnotes/group', headers=self.headers, sid=self.sid1, data={
            "groupId": data_msg_group[0]["groupId"],
            "startIndex": 0,
            "rows": -100
        }, )
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMessage": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase06_GetNotesForGroupFailed(self):
        """查看分组下标签,必填项groupId传int数据类型校验"""
        step("查看分组下的便签")
        res = post(url=self.host + '/v3/notesvr/web/getnotes/group', headers=self.headers, sid=self.sid1, data={
            "groupId": DataGenerator.generate_time_int(),
            "startIndex": 0,
            "rows": 20
        })
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -2009, "errorMessage": "参数不正确"}
        CheckOutput().output_check(expect=expect, actual=res.json())

    def testCase07_GetNotesForGroupFailed(self):
        """查看分组下标签,必填项groupId传不存在的特殊字符校验"""
        step("查看分组下的便签")
        res = post(url=self.host + '/v3/notesvr/web/getnotes/group', headers=self.headers, sid=self.sid1, data={
            "groupId": "￥%#%……&",
            "startIndex": 0,
            "rows": 20
        })
        self.assertEqual(500, res.status_code)
        expect = {"errorCode": -1002, "errorMessage": "GroupId Not Exist!"}
        CheckOutput().output_check(expect=expect, actual=res.json())
