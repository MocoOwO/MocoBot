import json

from . import eventclass,CONFIG
import requests

Host = CONFIG.Host


def MsgLog(data: eventclass.Message):
    if isinstance(data, eventclass.PrivateMessage):
        print(
            f"[MocoBot][Msg] 收到好友 {data.sender['nickname']}({data.sender['user_id']}) 的消息: {data.raw_message} ")
    elif isinstance(data, eventclass.GroupMessage):
        d = requests.get(f"{Host}get_group_info?group_id={data.group_id}").text
        name = json.loads(d)['data']['group_name']
        print(f"[MocoBot][Msg] 收到群 {name}({data.group_id}) 内 {data.sender['nickname']}"
              f"({data.sender['user_id']}) 的消息: {data.raw_message}")
