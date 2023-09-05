import os
import sys
import time

import prettytable
from . import Color
from . import  Init


# os.get_terminal_size()获取长宽

def load(path, AddPath: bool = True, Echo: bool = False):
    time.sleep(0.5)
    print("[MocoBot][Plugin] 正在加载插件...")
    if AddPath:
        sys.path.append(os.path.join(os.path.dirname(__file__), f'../{path}'))
        # print(sys.path)
    d = os.listdir(path)
    pl = []
    l = []
    for i in d:
        if os.path.isdir(path + i) == True:
            l.append(i)
    for i in range(l.count('__pycache__')):
        l.remove('__pycache__')

    # load 完成
    for i in l:
        if AddPath:
            pl.append(__import__(i))
        else:
            pl.append(__import__(path[2:-1] + "." + i, None, None, i))

    print("[MocoBot][Plugin] 加载完成")
    if Echo:
        tb = prettytable.PrettyTable()
        tb.field_names = ["命名空间", "名称", "开发者", "版本"]
        for i in pl:
            if i.VersionCode == "NumList":
                tb.add_row([i.__name__, i.PluginName, i.Developer,f'{i.Version[0]}.{i.Version[1]}.{i.Version[2]}'])
            else:
                tb.add_row([i.__name__, i.PluginName, i.Developer,f'{i.Version}'])
        print(f"{Color.Fore.GREEN}{tb.get_string()}")

    return pl
