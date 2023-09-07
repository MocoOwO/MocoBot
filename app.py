import time
from concurrent.futures import ThreadPoolExecutor, as_completed

from Builtin import eventclass, CONFIG
import logging
import Builtin
from flask import Flask, request

app = Flask(__name__)

FirstStart = True
# 禁用FlaskLog
log = logging.getLogger('werkzeug')
log.disabled = True
MAX_WORKER = 16
Host = CONFIG.Host
PluginPATH = "./Plugin/"

pool = ThreadPoolExecutor(max_workers=MAX_WORKER)

pl = []
Log = True


def FindReply(data, pl):
    global Log
    Log = True
    for i in pl:
        if i.HaveReply:
            if i.IsReply(data):
                i.Reply(data, Host)
                if i.HaveLog:
                    Log = False
    if Log:
        Builtin.Log(data)


# pool.submit(lambda p: a(*p),[4,5,6])

@app.route('/', methods=["GET", "POST"])
def main_task():
    global FirstStart
    if FirstStart:
        if Builtin.InitFin is False:
            pool.submit(Builtin.init, True)
        global pl
        pl = Builtin.g(PluginPATH, False, True)
        FirstStart = False
    data = eventclass.find_event_class(request.json)
    if isinstance(data, eventclass.Request):
        if isinstance(data, eventclass.GroupRequest):
            print(data.flag)
        pass
    elif isinstance(data, eventclass.Notice):
        pass
    elif isinstance(data, eventclass.Message):
        Builtin.MsgDB(data)
        if isinstance(data, eventclass.GroupMessage):
            if data.group_id != 830813843:
                pool.submit(FindReply, data, pl)
        else:
            print(FindReply,data,pl)

    # print(type(data))
    return """{
    "status": "ok",
    "retcode": 0
}"""


if __name__ == '__main__':
    # init()
    app.run(host="127.0.0.1", port=15700, debug=True)
