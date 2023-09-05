from colorama import init, Fore, Back, Style

color = {
    "reset": Fore.RESET + Style.RESET_ALL + Back.RESET,
    "red": Fore.RED,
    "green": Fore.GREEN,
    "yellow": Fore.YELLOW,
    "black": Fore.BLACK,
    "blue": Fore.BLUE,
    "cyan": Fore.CYAN,
    "magenta": Fore.MAGENTA,
    "white": Fore.WHITE,
    "bright_red": Style.BRIGHT + Fore.RED,
    "bright_green": Style.BRIGHT + Fore.GREEN,
    "bright_yellow": Style.BRIGHT + Fore.YELLOW,
    "bright_black": Style.BRIGHT + Fore.BLACK,
    "bright_blue": Style.BRIGHT + Fore.BLUE,
    "bright_cyan": Style.BRIGHT + Fore.CYAN,
    "bright_magenta": Style.BRIGHT + Fore.MAGENTA,
    "bright_whit": Style.BRIGHT + Fore.WHITE
}


def printer(c, string):
    if c in color:
        print(f"{color[c]}{string}")
    else:
        print(f"{color['white']}{string}")
    print(Fore.RESET + Back.RESET + Style.RESET_ALL)


if __name__ == "__main__":
    init(autoreset=True)  # 初始化，并且设置颜色设置自动恢复
    for key in color:
        print(f"{color[key]}{key} color is this")
    # 如果未设置autoreset=True，需要使用如下代码重置终端颜色为初始设置
    # print(Fore.RESET + Back.RESET + Style.RESET_ALL)  autoreset=True
    print('back to normal now')
