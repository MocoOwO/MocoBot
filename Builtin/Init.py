import json
import os
import sqlite3
import prettytable
import requests
from . import Color, CONFIG
import platform

Host = CONFIG.Host

global InitFin

InitFin = False

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

def init(Echo=True):
    if platform.system()=="Windows":
        os.system("cls")
        os.system("title MocoBot")
    elif platform.system()=="Linux":
        os.system("clear")
    r = requests.get(Host + 'get_login_info')
    d = json.loads(r.text)['data']
    print(f"[MocoBot][Info] 连接到{d['nickname']}({d['user_id']})")

    # 加载好友列表
    if platform.system() == "Windows":
        friends_db = sqlite3.connect(r".\db\friends.db")
    elif platform.system() == "Linux":
        friends_db = sqlite3.connect(r"./db/friends.db")
    friends_cur = friends_db.cursor()
    friends_cur.execute("""CREATE TABLE IF NOT EXISTS FRIENDS
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL);""")
    print("[MocoBot][Init] 加载好友列表...")
    r = requests.get(Host + 'get_friend_list')
    d = json.loads(r.text)
    tb = prettytable.PrettyTable()
    tb.field_names = ["QQ号", "名称"]
    for i in d['data']:
        tb.add_row([i['user_id'], i['nickname']])
        try:
            friends_cur.execute(DBStr(f"""INSERT INTO FRIENDS (ID, NAME) values ({i['user_id']}, \"{i['nickname']}\");"""))
        except sqlite3.IntegrityError:
            friends_cur.execute(DBStr(f"UPDATE FRIENDS SET NAME = \"{i['nickname']}\" where ID={i['user_id']}"))
        # print(f"{Builtin.Color.Fore.RED}{i['nickname']}{i['user_id']}")
    print("[MocoBot][Init] 加载完成")
    friends_db.commit()
    friends_db.close()
    if Echo:
        print(f"{Color.Fore.GREEN}{tb.get_string()}")

    # 获取群列表
    if platform.system() == "Windows":
        groups_db = sqlite3.connect(r".\db\groups.db")
    elif platform.system() == "Linux":
        groups_db = sqlite3.connect(r"./db/groups.db")
    groups_cur = groups_db.cursor()
    groups_cur.execute("""CREATE TABLE IF NOT EXISTS GROUPS
       (ID INT PRIMARY KEY     NOT NULL,
       NAME           TEXT    NOT NULL,
       MAXNUM         INT NOT NULL,
       NUM         INT NOT NULL);""")
    print("[MocoBot][Init] 加载群列表...")
    r = requests.get(Host + 'get_group_list')
    tb2 = prettytable.PrettyTable()
    tb2.field_names = ["群号", "群名称", "群人数"]
    for i in json.loads(r.text)['data']:
        tb2.add_row([i['group_id'], i['group_name'], f"{i['member_count']}/{i['max_member_count']}"])
        try:
            groups_cur.execute(DBStr(f"""INSERT INTO GROUPS (ID, NAME, MAXNUM, NUM) 
            values ({i['group_id']}, \"{i['group_name']}\", {i['max_member_count']} ,{i['member_count']});"""))
        except sqlite3.IntegrityError:
            groups_cur.execute(DBStr(f"UPDATE GROUPS SET NAME = \"{i['group_name']}\" where ID={i['group_id']}"))
            groups_cur.execute(DBStr(f"UPDATE GROUPS SET MAXNUM = {i['max_member_count']} where ID={i['group_id']}"))
            groups_cur.execute(DBStr(f"UPDATE GROUPS SET NUM = {i['member_count']} where ID={i['group_id']}"))
        _GroupDetail(i['group_id'], groups_cur)
        groups_db.commit()
        # print(i['group_id'], i['group_name'], i['max_member_count'], i['member_count'])
    print("[MocoBot][Init] 加载完成")
    groups_db.commit()
    groups_db.close()
    if Echo:
        print(f"{Color.Fore.GREEN}{tb2.get_string()}")
    InitFin = True


def _GroupDetail(group_id: int, cur):
    r = requests.get(Host + f'get_group_member_list?group_id={group_id}')
    d = json.loads(r.text)['data']
    cur.execute(f"""CREATE TABLE IF NOT EXISTS G{group_id}
    (ID INT PRIMARY KEY     NOT NULL,
           NAME           TEXT    NOT NULL,
           ROLE         INT NOT NULL);""")
    for i in d:
        if i['role'] == 'member':
            role = 0
        elif i['role'] == 'admin':
            role = 1
        elif i['role'] == 'owner':
            role = 2

        # print(f"{i['nickname']} {i['user_id']} {role}")
        try:
            cur.execute(f"""INSERT INTO G{group_id} (ID, NAME, ROLE) 
            values ({i['user_id']}, \"{i['nickname']}\", {role} );""")
        except sqlite3.IntegrityError:
            cur.execute(f"UPDATE G{group_id} SET NAME = \"{i['nickname']}\" where ID={i['user_id']}")
            cur.execute(f"UPDATE G{group_id} SET ROLE = {role} where ID={i['user_id']}")
