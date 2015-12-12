from PyQt5 import QtWidgets, QtCore
from ui import Ui_AddTag, Ui_Manage
import os
import sys
import fileTagger
import reg
import scanner

fileTagger = fileTagger.FileTagger.getInstance()


class ManageDialog(object):

    """docstring for ManageDialog"""

    def __init__(self, path):
        scanner.scan(fileTagger.taggerManager, path, self.event_scanFinished)
        self.path = path
        self.basename = os.path.basename(path)
        self.__loadUI()
        self.pathLabel.setText(self.basename)
        self.pathLabel.setToolTip(self.path)

        self.resource = fileTagger.taggerManager.registerTagger(self.path)
        self.__setTagLabel()
        self.resultList = {}

    def event_manage(self):
        item = self.__getResultItem()
        if item and not item.isFile:
            self.dialog.accept()
            self.__manage = ManageDialog(item.path)
            self.__manage.show()

    def __setTagLabel(self):
        tags = self.resource.getDirTags()
        self.tagLabel.setText(', '.join(tags))

    def __loadUI(self):
        self.dialog = QtWidgets.QDialog()
        window = Ui_Manage()
        window.setupUi(self.dialog)

        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.pathLabel = window.pathLabel
        self.tagLabel = window.tagLabel
        self.tagEditLabel = window.tagEditLabel
        self.msgLabel = window.msgLabel

        self.tagEditLabel.linkActivated['QString'].connect(self.event_editTag)

        self.searchEdit = window.searchEdit
        self.searchBox = window.searchBox
        self.searchButton = window.searchButton

        self.searchButton.clicked.connect(self.event_search)
        self.searchEdit.returnPressed.connect(self.event_search)

        self.searchList = window.searchList
        self.openButton = window.openButton
        self.editButton = window.editButton
        self.manageButton = window.manageButton

        setWidth = self.searchList.setColumnWidth
        [setWidth(i, w) for i, w in enumerate([244, 65, 370])]

        self.searchList.itemSelectionChanged.connect(self.event_activate)
        self.searchList.itemDoubleClicked[
            'QTreeWidgetItem*', 'int'].connect(self.event_openButton)
        self.openButton.clicked.connect(self.event_openButton)
        self.editButton.clicked.connect(self.event_editButton)
        self.manageButton.clicked.connect(self.event_manage)

        self.regBox = window.regBox
        registered, permission = reg.check()
        if permission:
            self.regBox.setEnabled(True)
            self.regBox.clicked.connect(self.event_reg)
        self.regBox.setCheckState(2 if registered else 0)

    def event_reg(self):
        # 状态已改变
        state = self.regBox.checkState()
        try:
            self.regBox.setCheckState(2 - state)
            reg.reg(sys.argv[0]) if state else reg.unreg()
            self.regBox.setCheckState(state)
        except FileNotFoundError:
            self.regBox.setCheckState(state)
        except PermissionError:
            self.regBox.setText("无管理员权限")
        except BaseException as e:
            self.regBox.setText("未知错误")
            self.regBox.setToolTip(str(e))
        finally:
            pass

    def show(self):
        self.dialog.show()

    def setMsg(self, msg):
        self.msgLabel.setText(msg)

    def event_editTag(self):
        self.__addTag = AddTagDialog(self.path, False)
        self.__addTag.dialog.finished.connect(self.__setTagLabel)
        self.__addTag.show()

    def event_search(self):
        self.searchList.clear()
        self.resultList = {}
        [w.setEnabled(False)
         for w in [self.editButton, self.manageButton, self.openButton]]
        tagText = self.searchEdit.text()
        tags = tagText.split()
        mode = self.searchBox.currentText()
        results = fileTagger.search(tags, mode)
        self.setMsg("搜索到%d处资源:" % len(results))
        [ResultItem(self, resource) for resource in results]

    def __getResultItem(self):
        item = self.searchList.selectedItems()
        if not item:
            return
        item = item[0]
        for k, v in self.resultList.items():
            if v == item:
                return k
        return None

    def event_activate(self, **argv):
        item = self.__getResultItem()
        if item:
            self.openButton.setEnabled(True)
            self.editButton.setEnabled(True)
            self.manageButton.setEnabled(not item.isFile)

    def event_openButton(self):
        item = self.__getResultItem()
        if item:
            if item.isFile:
                os.popen(item.path)
            else:
                os.popen("explorer.exe /e, {path}".format(path=item.path))

    def event_editButton(self):
        item = self.__getResultItem()
        if item:
            self.__addTag = AddTagDialog(item.path, item.isFile)
            self.__addTag.dialog.finished.connect(item.updateTags)
            self.__addTag.show()

    def event_scanFinished(self, info):
        self.setMsg(info)


class ResultItem(object):

    """docstring for ResultItem"""

    def __init__(self, dialog, resource):
        self.dialog = dialog
        self.path = resource.path
        self.basename = resource.basename
        self.isFile = resource.isFile
        self.resource = resource

        item = QtWidgets.QTreeWidgetItem(self.dialog.searchList)
        item.setText(0, self.basename)
        item.setToolTip(0, self.path)
        item.setText(1, "文件" if self.isFile else "文件夹")
        item.setText(2, ", ".join(self.getTags()))

        dialog.resultList[self] = item
        self.item = item

    def getTags(self):
        return self.resource.getTags()

    def updateTags(self):
        self.item.setText(2, ", ".join(self.getTags()))


class AddTagDialog(object):

    """docstring for AddTag"""

    def __init__(self, path, isFile=True):
        self.path = path
        self.basename = os.path.basename(path)
        self.__loadUI()
        self.pathLabel.setText(self.basename)
        self.pathLabel.setToolTip(self.basename)

        self.resource = fileTagger.getBaseResource(path, isFile)
        tags = self.resource.getTags()
        [self.addItem(tag) for tag in tags]

    # 加载由pyuic5转换来的ui_add.py
    def __loadUI(self):
        self.dialog = QtWidgets.QDialog()
        window = Ui_AddTag()
        window.setupUi(self.dialog)

        self.dialog.setWindowFlags(QtCore.Qt.WindowCloseButtonHint)

        self.pathLabel = window.pathLabel
        self.tagList = window.tagList
        self.tagEdit = window.tagEdit
        self.addButton = window.addButton
        self.saveButton = window.saveButton

        self.tagEdit.returnPressed.connect(self.event_add)
        self.addButton.clicked.connect(self.event_add)
        self.saveButton.clicked.connect(self.dialog.accept)
        self.tagList.itemDoubleClicked[
            'QListWidgetItem*'].connect(self.event_toggle)  # 见到这种语句也是醉了
        self.dialog.finished.connect(self.event_save)

    def getItem(self, tag):
        item = self.tagList.findItems(tag, QtCore.Qt.MatchFlags())
        if item:
            return item[0]
        else:
            return QtWidgets.QListWidgetItem(self.tagList)

    def addItem(self, tag, checked=True):
        checked = QtCore.Qt.Checked if checked else QtCore.Qt.Unchecked
        item = self.getItem(tag)
        item.setCheckState(checked)
        item.setText(tag)
        self.focus(item)
        return item

    def show(self):
        self.dialog.show()

    def focus(self, item):
        n = self.tagList.count()
        items = [self.tagList.item(i) for i in range(0, n)]

        [i.setSelected(False) for i in items]
        item.setSelected(True)

        index = items.index(item)
        # pos = 0 if index <= 7 else index - 7
        pos = self.tagList.verticalScrollBar().value()
        offset = 0 if pos <= index <= pos + 7 else index - pos
        offset += -7 if index > pos + 7 else 0
        self.tagList.verticalScrollBar().setValue(pos + offset)

    def event_toggle(self):
        item = self.tagList.selectedItems()[0]
        checked = item.checkState()
        if checked == QtCore.Qt.Checked:
            checked = QtCore.Qt.Unchecked
        else:
            checked = QtCore.Qt.Checked
        item.setCheckState(checked)

    def event_add(self):
        tagText = self.tagEdit.text()
        if tagText:
            [self.addItem(tag) for tag in filter(None, tagText.split(' '))]
            self.tagEdit.setText('')

    def event_save(self):
        tags = []
        n = self.tagList.count()
        items = [self.tagList.item(i) for i in range(0, n)]
        [item.checkState() and tags.append(item.text()) for item in items]
        self.resource.setTags(tags)
        self.resource.save()
