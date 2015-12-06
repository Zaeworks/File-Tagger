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
    runPath = "python " if path[-4:] == ".pyw" else ""
    runPath += '"{path}"'.format(path=path)

    command = "{run} -a -f %1".format(run=runPath)
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "*\shell")
    key = winreg.CreateKey(key, "File Tagger")
    winreg.SetValue(key, "", 1, "添加/移除标签...")
    key = winreg.CreateKey(key, "Command")
    winreg.SetValue(key, "", 1, command)

    command = "{run} -m %1".format(run=runPath)
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Folder\shell")
    key = winreg.CreateKey(key, "File Tagger")
    winreg.SetValue(key, "", 1, "标签式管理...")
    key = winreg.CreateKey(key, "Command")
    winreg.SetValue(key, "", 1, command)

    command = "{run} -m %V".format(run=runPath)
    key = winreg.OpenKey(
        winreg.HKEY_CLASSES_ROOT, "Directory\Background\shell")
    key = winreg.CreateKey(key, "File Tagger")
    winreg.SetValue(key, "", 1, "标签式管理...")
    key = winreg.CreateKey(key, "Command")
    winreg.SetValue(key, "", 1, command)


def unreg():
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "*\shell\File Tagger")
    winreg.DeleteKey(key, "Command")
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "*\shell")
    winreg.DeleteKey(key, "File Tagger")

    key = winreg.OpenKey(
        winreg.HKEY_CLASSES_ROOT, "Folder\shell\File Tagger")
    winreg.DeleteKey(key, "Command")
    key = winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, "Folder\shell")
    winreg.DeleteKey(key, "File Tagger")

    key = winreg.OpenKey(
        winreg.HKEY_CLASSES_ROOT, "Directory\Background\shell\File Tagger")
    winreg.DeleteKey(key, "Command")
    key = winreg.OpenKey(
        winreg.HKEY_CLASSES_ROOT, "Directory\Background\shell")
    winreg.DeleteKey(key, "File Tagger")


def check():
    keys = ["*\shell\File Tagger", "Folder\shell\File Tagger",
            "Directory\Background\shell\File Tagger"]
    registered, permission = True, True
    try:
        [winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, key) for key in keys]
    except FileNotFoundError:
        registered = False

    try:
        winreg.OpenKey(winreg.HKEY_CLASSES_ROOT, keys[0], access=winreg.KEY_WRITE)
    except PermissionError:
        permission = False
    return registered, permission
