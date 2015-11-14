# reg.py -- FileTagger 注册表模块

import winreg

lang = {
    "reg_title": "添加/移除标签...",
}


def regedit(act, path=None):
    result = ()
    try:
        act(path) if path else act()
        result = (True, "")
    except FileNotFoundError:
        result = (True, "无需清理注册表")
    except PermissionError:
        result = (False, "注册表拒绝访问,请用管理员身份运行并执行此操作")
    except BaseException as e:
        result = (False, "未知错误({info})".format(info=str(e)))
    finally:
        return result


def reg(path):
    if path[-3:] == ".py":
        command = "python {path} quickadd %1".format(path=path)
    else:
        command = "{path} quickadd %1".format(path=path)

    for regPath in ["*\shell", "Directory\shell"]:
        key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, regPath)
        key = winreg.CreateKey(key, "File Tagger")
        winreg.SetValue(key, "", 1, "添加/移除标签...")
        key = winreg.CreateKey(key, "Command")
        winreg.SetValue(key, "", 1, command)


def unreg():
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "*\shell\File Tagger")
    winreg.DeleteKey(key, "Command")
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "*\shell")
    winreg.DeleteKey(key, "File Tagger")

    key = winreg.OpenKey(
        winreg.HKEY_CLASSES_ROOT, "Directory\shell\File Tagger")
    winreg.DeleteKey(key, "Command")
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Directory\shell")
    winreg.DeleteKey(key, "File Tagger")
