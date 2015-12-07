import os
import threading
from time import time

keyword = '.fileTagger'


def scanStart(taggerManager, path, callback=None):
    timecount = time()
    taggers = scanIt(taggerManager, path)
    timecount = time() - timecount
    info = "扫描到 %d 个标签目录, 用时 %.1f秒" % (taggers, timecount)
    callback and callback(info)


def scanIt(taggerManager, path):
    count = 0
    try:
        listdir = os.listdir(path)
    except PermissionError:
        pass
    else:
        for f in listdir:
            newPath = os.path.join(path, f)
            if os.path.isdir(newPath):
                count += scanIt(taggerManager, newPath)
            elif keyword == f:
                count += 1
                taggerManager.registerTagger(path)
    finally:
        return count


def scan(taggerManager, path, callback):
    t = threading.Thread(
        target=scanStart, args=(taggerManager, path, callback))
    t.start()
