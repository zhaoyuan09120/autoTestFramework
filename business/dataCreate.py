import requests
from common.dataGenerator import DataGenerator
from common.yamlRead import YamlRead


class DataCreate:
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}", "Content-Type": "application/json", }

    def create_note(self, num):
        """不指定分组创建便签"""
        notes_list = []
        for i in range(num):
            body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId"}
            res = requests.post(url=self.host + '/v3/notesvr/set/noteinfo', headers=self.headers, json=body_main)
            infoVersion = res.json()['infoVersion']
            body_content = {
                "noteId": body_main["noteId"],
                "title": "test",
                "summary": "test",
                "body": "test",
                "localContentVersion": infoVersion,
                "BodyType": 0
            }
            notes_list.append(body_content)
            requests.post(url=self.host + '/v3/notesvr/set/notecontent', headers=self.headers, json=body_content)
        return notes_list

    def create_note_for_group(self, group_id, num):
        """指定分组下创建便签"""
        note_for_group_list = []
        for i in range(num):
            body_main = {"noteId": DataGenerator.generate_time_str() + "_noteId", "groupId": group_id}
            res = requests.post(url=self.host + '/v3/notesvr/set/noteinfo', headers=self.headers, json=body_main)
            infoVersion = res.json()['infoVersion']
            body_content = {
                "noteId": body_main["noteId"],
                "title": "test",
                "summary": "test",
                "body": "test",
                "localContentVersion": infoVersion,
                "BodyType": 0
            }
            note_for_group_list.append(body_content)
            requests.post(url=self.host + '/v3/notesvr/set/notecontent', headers=self.headers, json=body_content)
        return note_for_group_list

    def create_group(self, order, num):
        """创建分组"""
        groups_list = []
        for i in range(num):
            body = {"groupId": DataGenerator.generate_time_str() + "_groupId",
                    "groupName": DataGenerator.generate_time_str() + "_groupName", "order": order}
            requests.post(url=self.host + '/v3/notesvr/set/notegroup', headers=self.headers, json=body)
            groups_list.append(body)
        return groups_list
