import json
import requests

from . import CONFIG

Host = CONFIG.Host


# 个人信息相关操作
def GetLoginInfo() -> dict:
    r = requests.get(Host + "get_login_info")
    return json.loads(r.text)


def SetQQProfile(nickname="", company="", email="", college="", personal_note="") -> None:
    f = False
    d = {}
    if nickname:
        f = True
        d.update({"nickname": nickname})
    if company:
        f = True
        d.update({"company": company})
    if email:
        f = True
        d.update({"email": email})
    if college:
        f = True
        d.update({"college": college})
    if personal_note:
        f = True
        d.update({"personal_note": personal_note})

    if f:
        requests.post(Host + "set_qq_profile", json=d)


def QiDianGetAccountInfo() -> dict:
    r = requests.get(Host + "qidian_get_account_info")
    return json.loads(r.text)


def GetModelShow(model: str) -> dict:
    d = {
        "model": model
    }
    r = requests.get(Host + "_get_model_show", json=d)
    return json.loads(r.text)


def SetModelShow(model: str, model_show: str) -> None:
    d = {
        "model": model,
        "model_show": model_show
    }
    r = requests.get(Host + "_set_model_show", json=d)


def GetOnlineClients() -> dict:
    r = requests.get(Host + "get_online_clients")
    return json.loads(r.text)


def SendMsg(msg, id, type) -> dict:
    if type == "group":
        d = {
            "group_id": id,
            "message": msg
        }
        r = requests.post(Host + "send_group_msg", json=d)
    else:
        d = {
            "user_id": id,
            "message": msg
        }
        r = requests.post(Host + "send_private_msg", json=d)

    # TODO:新作响应对象
    return json.loads(r.text)
