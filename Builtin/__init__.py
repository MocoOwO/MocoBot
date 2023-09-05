from . import ColorPrinter as Color
from . import Init
from . import Log as log
from . import PluginLoader
from . import MsgDB as M

Color.init(autoreset=True)

cPrint = Color.printer
init = Init.init
Log = log.MsgLog

g = PluginLoader.load
InitFin = Init.InitFin
MsgDB = M.MsgDB