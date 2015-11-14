# -*- encoding: utf-8 -*-
# init via cmd

import fileTagger
import sys
import os
import reg

tempList = {}


def search(args=None):
    if args:
        mode = "and"
        if args[0] == "--or":
            mode = "or"
            args = args[1:]
        fileList = fileTagger.FileTagger.getInstance().search(args, mode)
        makeTempList(fileList)

        # print(" > ----------------------------------")
        for i, path in tempList.items():
            print("[{index}]{name} > {path}".format(
                index=i, name=os.path.basename(path), path=path))
        print(" > --- 输入open [编号] 打开相应资源 ---")
    else:
        print("使用 > search (--or) 标签1 (标签2) (标签3) (...)")
        print("默认为and模式,输入--or参数使用or模式")


def quickadd(path):
    # path = path.encode('gbk', 'ignore').decode('gbk')
    os.system("title FileTagger - " + path)
    print("快速标签 > " + os.path.basename(translate(path)))
    print("多个标签用空格隔开,如移除标签请使用--r参数")
    tags = getVaildInput("请输入标签:")
    fTagger = fileTagger.FileTagger()
    isFile = os.path.isfile(path)
    func = fTagger.addTagToFile if isFile else fTagger.addTagToDir
    if tags[0] == "--r":
        tags = tags[1:]
        func = fTagger.removeTagFromFile if isFile else fTagger.removeTagToDir
    for tag in tags:
        func(path, tag)
    input("操作完毕,按回车键退出")


def cmdControl():
    cmd = getVaildInput("\nFileTagger > ")
    if cmd[0] == "search":
        search(cmd[1:])
    elif cmd[0] == "open":
        index = int(cmd[1])
        if index in tempList.keys():
            if os.path.isfile(tempList[index]):
                os.popen(tempList[index])
            else:
                os.popen(
                    "explorer.exe /e, {path}".format(path=tempList[index]))
    elif cmd[0] == "reg" or cmd[0] == "unreg":
        if cmd[0] == "reg":
            result, info = reg.regedit(reg.reg, os.path.abspath(FILEPATH))
        else:
            result, info = reg.regedit(reg.unreg)
        text = "操作完毕." if result else "操作失败"
        text += " > {info}".format(info=info) if info else ""
        print(text)
    elif cmd[0] == "help":
        print("""search > 按标签搜索
open > 快速打开搜索结果中的匹配项
reg/unreg > 开关快速标签功能(管理员)
exit > 退出""")
    elif cmd[0] == "exit":
        return True


def getVaildInput(text, warningText=None):
    cmd = input(text)
    if cmd:
        return cmd.split()
    else:
        print(warningText) if warningText else False
        return getVaildInput(text, warningText)


def makeTempList(newlist):
    global tempList
    tempList = {}
    for i in range(0, len(newlist)):
        tempList[i + 1] = newlist[i]


def translate(path):
    return path.encode('gbk', 'ignore').decode('gbk')


if __name__ == "__main__":
    argv = sys.argv
    FILEPATH = argv[0]
    os.system("title File Tagger")
    if argv[1:] and argv[1] == "quickadd":
        # quickadd(argv[3], True if argv[2] == "file" else False)
        quickadd(' '.join(argv[2:]))
    else:
        print(" > File Tagger - 标签式资源管理器")
        print(" > Author: 扎易@Zaeworks")
        print(" > 输入help查看帮助")
        while cmdControl() is not True:
            pass
