import requests


def SendMsg(msg, Host, id, type):
    if type == "group":
        d = {
            "group_id": id,
            "message": msg
        }
        requests.post(Host + "send_group_msg", json=d)
    else:
        d = {
            "user_id": id,
            "message": msg
        }
        requests.post(Host + "send_private_msg", json=d)
