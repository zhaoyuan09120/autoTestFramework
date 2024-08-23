import unittest
from business.dataClear import DataClear
from common.checkOutput import CheckOutput
from common.logsMethod import class_case_log, step
from business.apiRe import post, get
from common.yamlRead import YamlRead
from common.dataGenerator import DataGenerator
from business.dataCreate import DataCreate


@class_case_log
class GetNotesForGroupMajor(unittest.TestCase):
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def setUp(self):
        """前置清理便签和分组"""
        DataClear().note_clear()
        DataClear().group_clear()

    def tearDown(self):
        """后置清理便签和分组"""
        DataClear().note_clear()
        DataClear().group_clear()

    def testCase01_GetNotesForGroupSuccessMajor(self):
        """查看分组下标签"""
        step("前置1：创建分组")
        data_msg_group = DataCreate().create_group(order=0,num=1)
        step("前置2：在step1创建的分组下构建便签主体、内容")
        data_msg_note = DataCreate().create_note_for_group(group_id=data_msg_group[0]['groupId'], num=1)
        step("查看分组下的便签")
        res = post(url=self.host + '/v3/notesvr/web/getnotes/group', headers=self.headers, sid=self.sid1, data={
            "groupId": data_msg_group[0]["groupId"],
            "startIndex": 0,
            "rows": 20
        })
        expect = {"responseTime": int, "webNotes": [
            {"noteId": data_msg_note[0]['noteId'], "groupId": data_msg_group[0]["groupId"],
             "title": data_msg_note[0]["title"], "summary": data_msg_note[0]["summary"], "thumbnail": None,
             "contentVersion": 1, "contentUpdateTime": int, "createTime": int, "star": 0, "remindTime": int,
             "remindType": 0, "infoVersion": 1, "infoUpdateTime": int}]}
        self.assertEqual(200, res.status_code)
        CheckOutput().output_check(expect=expect, actual=res.json())
