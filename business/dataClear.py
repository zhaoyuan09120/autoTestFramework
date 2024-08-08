import requests

from common.yamlRead import YamlRead


class DataClear:
    envConfig = YamlRead().env_config()
    userid1 = envConfig['userid1']
    sid1 = envConfig['sid1']
    host = envConfig['host']
    headers = {"Cookie": f"wps_sid={sid1}", "X-user-key": f"{userid1}"}

    def group_clear(self):
        """获取当前所有有效的分组列表"""
        data = {"excludeInValid": True}
        get_res = requests.post(url=self.host + "/v3/notesvr/get/notegroup", headers=self.headers, json=data)
        for group in get_res.json()["noteGroups"]:
            group_id = group['groupId']
            data = {"groupId": group_id}
            del_res = requests.post(url="http://note-api.wps.cn/notesvr/delete/notegroup", headers=self.headers,
                                    json=data)
            if del_res.status_code != 200:
                return False
        return True

    def note_clear(self):
        """软删除便签（首页便签、分组便签）"""
        get_res = requests.get(url=self.host + f'/v3/notesvr/user/{self.userid1}/home/startindex/0/rows/50/notes',
                               headers=self.headers)
        for note in get_res.json()["webNotes"]:
            note_id = note['noteId']
            data = {"noteId": note_id}
            del_res = requests.post(url=self.host + "/v3/notesvr/delete", headers=self.headers, json=data)
            if del_res.status_code != 200:
                return False
        return True

    def recycle_bin_note_clear(self):
        """彻底删除回收站的所有便签"""
        body = {"noteIds": ["-1"]}
        try:
            res = requests.post(url=self.host + '/v3/notesvr/cleanrecyclebin', headers=self.headers, json=body)
        except Exception as e:
            raise e
        if res.status_code != 200:
            return True
        return False


if __name__ == '__main__':
    sid = 'V02Sw-JSqZJ06TWVRk0KaVv-ryEtLj800a4d0a690014151d2c'
    userid = '336928044'
    DataClear().note_clear()
