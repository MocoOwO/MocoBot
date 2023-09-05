import platform
import sqlite3
import time
from . import eventclass



def DBStr(s: str):
    s.replace("/", "//")
    s.replace("'", "''")
    s.replace("[", '/[')
    s.replace("]", '/]')
    s.replace("%", '/%')
    s.replace("&", '/&')
    s.replace("_", '/_')
    s.replace("(", '/(')
    s.replace(")", '/)')
    return s


def MsgDB(data: eventclass.Message):
    if platform.system()=="Windows":
        Msg_db = sqlite3.connect(r".\db\message.db")
    elif platform.system()=="Linux":
        Msg_db = sqlite3.connect(r"./db/message.db")
    Msg_cur = Msg_db.cursor()
    if isinstance(data, eventclass.GroupMessage):
        Msg_cur.execute(f"""CREATE TABLE IF NOT EXISTS G{data.group_id}
                        (MSGID INT PRIMARY KEY     NOT NULL,
                        NAME           TEXT    NOT NULL,
                        MSG             TEXT    Not NULL,
                        USERID             INT    Not NULL,
                        TIME            INT    Not NULL,
                        STRTIME            INT    Not NULL);""")
        if data.anonymous == None:
            Msg_cur.execute(
                f"""INSERT INTO G{data.group_id} (MSGID, NAME,MSG,USERID,TIME,STRTIME) values ({data.message_id}, \'{data.sender['nickname']}\',\'{DBStr(data.raw_message)}\',{data.user_id},{data.time},\'{time.strftime("%Y-%m-%d, %H:%M:%S", time.localtime(data.time))}\');""")
    Msg_db.commit()
    Msg_db.close()
