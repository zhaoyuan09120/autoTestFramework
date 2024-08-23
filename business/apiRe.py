import requests
from common.logsMethod import info, error


def get(url, sid, headers=None):
    if headers is None:
        headers = {"Cookie": f"wps_sid={sid}"}
    info(f"【requests】url：{url}")
    info(f"【requests】headers：{headers}")
    try:
        res = requests.get(url=url, headers=headers)
    except TimeoutError:
        error("requests timeout!")
    info(f"【response】code：{res.status_code}")
    info(f"【response】body：{res.text}")
    return res


def post(url, sid, data, headers=None):
    if headers is None:
        headers = {"Cookie": f"wps_sid={sid}"}
    info(f"【requests】url：{url}")
    info(f"【requests】headers：{headers}")
    info(f"【requests】body：{data}")
    try:
        res = requests.post(url=url, headers=headers, json=data, timeout=30)
    except TimeoutError:
        error("requests timeout!")
    info(f"【response】code：{res.status_code}")
    info(f"【response】body：{res.text}")
    return res


def patch(url, sid, data, headers=None):
    if headers is None:
        headers = {"Cookie": f"wps_sid={sid}"}
    info(f"【requests】url：{url}")
    info(f"【requests】headers：{headers}")
    info(f"【requests】body：{data}")
    try:
        res = requests.patch(url=url, headers=headers, json=data, timeout=30)
    except TimeoutError:
        error("requests timeout!")
    info(f"【response】code：{res.status_code}")
    info(f"【response】body：{res.text}")
    return res


def delete():
    pass



