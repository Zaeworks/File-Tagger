import os
import threading
from time import time

keyword = '.fileTagger'


def scanStart(taggerManager, path, callback):
    timecount = time()
    taggers = scanIt(taggerManager, path)
    timecount = time() - timecount
    info = "扫描到 %d 个标签目录, 用时 %.1f秒" % taggers, timecount
    callback(info)


def scanIt(taggerManager, path):
    count = 0
    for f in os.listdir(path):
        newPath = os.path.join(path, f)
        if os.path.isdir(newPath):
            count += scanIt(taggerManager, newPath)
        elif keyword == f:
            count += 1
            taggerManager.registerTagger(path)
    return count


def scan(taggerManager, path, callback):
    t = threading.Thread(
        target=scanStart, args=(taggerManager, path, callback))
    t.start()
