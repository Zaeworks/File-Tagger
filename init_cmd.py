# -*- encoding: utf-8 -*-
# init via cmd

import fileTagger
import sys
import os
import reg
import scanner

tempList = []

FileTagger = fileTagger.FileTagger.getInstance()


def search(args=None):
    if not args:
        print("使用 > search (--or) 标签1 (标签2) (标签3) (...)")
        print("默认为and模式,输入--or参数使用or模式")
        return
    args, mode = (args, 'and') if args[0] != '--or' else (args[1:], 'or')
    resources = FileTagger.search(args, mode)

    def makeResourceTree():
        tree = {}
        for resource in resources:
            tagger = resource.tagger
            tagger not in tree and tree.update({tagger: []})
            if isinstance(resource, fileTagger.Folder):
                tree[tagger].insert(0, resource)
            else:
                tree[tagger].append(resource)
        return tree

    global tempList
    tempList = []
    tree = makeResourceTree()
    for tagger in tree.values():
        treePath = os.path.relpath(tagger[0].path)
        if len(tagger) == 1:
            print("[%d]%s" % (len(tempList), treePath))
            tempList.append(tagger[0])
        else:
            if isinstance(tagger[0], fileTagger.Folder):
                print("[%d]%s:" % (len(tempList), treePath))
                tempList.append(tagger[0])
                tagger = tagger[1:]
            else:
                print("%s:" % os.path.dirname(treePath))

            for res in tagger:
                print("        [%d]%s" % (len(tempList), res.basename))
                tempList.append(res)
    if tempList:
        print(" > --- 输入open [编号] 打开相应资源 ---")
    else:
        print(" > --- 无结果 ---")


def quickadd(path, isFile=True):
    # path = path.encode('gbk', 'ignore').decode('gbk') -- 弥天巨坑之编码
    resource = FileTagger.getBaseResource(path, isFile)
    os.system("title FileTagger - " + resource.path)
    print("快速标签 > " + translate(resource.basename))
    print("多个标签用空格隔开,如移除标签请使用--r参数")
    resource.getTags() and print("当前标签: " + ', '.join(resource.getTags()))
    tags = getVaildInput("请输入标签:")
    add, tags = (False, tags[1:]) if tags[0] == "--r" else (True, tags)
    [resource.setTag(tag, add) for tag in tags]
    resource.save()
    input("操作完毕,按回车键退出")


def addDirTag(tags=None):
    if tags:
        add, tags = (False, tags[1:]) if tags[0] == "--r" else (True, tags)
        [folderResource.setTag(tag, add) for tag in tags]
        folderResource.save()
        print("操作完毕.")
    else:
        print("使用 > tag (--r) 标签1 (标签2) (...)")
        print("输入--r可移除指定标签.")


def cmdControl():
    cmd = getVaildInput("\nFileTagger > ")
    if cmd[0] == "tag":
        addDirTag(cmd[1:])
    elif cmd[0] == "search":
        search(cmd[1:])
    elif cmd[0] == "open":
        index = int(cmd[1]) if cmd[1].isnumeric() else -1
        if 0 <= index < len(tempList):
            path = tempList[index].path
            if tempList[index].isFile:
                os.popen(path)
            else:
                os.popen("explorer.exe /e, {path}".format(path=path))
    elif cmd[0] == "reg" or cmd[0] == "unreg":
        if cmd[0] == "reg":
            result, info = reg.regedit(reg.reg, os.path.abspath(FILEPATH))
        else:
            result, info = reg.regedit(reg.unreg)
        text = "操作完毕." if result else "操作失败"
        text += " > {info}".format(info=info) if info else ""
        print(text)
    elif cmd[0] == "help":
        print("""tag > 给当前目录添加/移除标签
search > 按标签搜索
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
    if len(argv) > 3 and argv[1] == "-a":
        path = ' '.join(argv[3:])
        quickadd(path, argv[2] == '-f')
    else:
        if len(argv) > 2 and argv[1] == "-m":
            currentPath = ' '.join(argv[2:])
        else:
            currentPath = os.path.abspath("")
        os.chdir(currentPath)
        os.system("title File Tagger - " + currentPath)
        scanner.scan(FileTagger.taggerManager, currentPath)
        print(" > File Tagger - 管理目录")
        print(" > Author: 扎易@Zaeworks")
        print(" > 输入help查看帮助")
        folderResource = FileTagger.getBaseResource(currentPath, False)
        tags = folderResource.getTags()
        if tags:
            print("当前目录标签: " + ', '.join(tags))
        while cmdControl() is not True:
            pass
