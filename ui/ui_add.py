# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui_add.ui'
#
# Created by: PyQt5 UI code generator 5.5.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddTag(object):
    def setupUi(self, AddTag):
        AddTag.setObjectName("AddTag")
        AddTag.resize(273, 275)
        AddTag.setMinimumSize(QtCore.QSize(273, 275))
        AddTag.setMaximumSize(QtCore.QSize(273, 275))
        AddTag.setStyleSheet("#AddTag{background-color: rgb(255, 255, 255)}")
        self.tagList = QtWidgets.QTreeWidget(AddTag)
        self.tagList.setGeometry(QtCore.QRect(10, 40, 251, 192))
        self.tagList.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.tagList.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tagList.setIndentation(22)
        self.tagList.setObjectName("tagList")
        self.tagEdit = QtWidgets.QLineEdit(AddTag)
        self.tagEdit.setGeometry(QtCore.QRect(10, 240, 113, 21))
        self.tagEdit.setInputMask("")
        self.tagEdit.setText("")
        self.tagEdit.setClearButtonEnabled(True)
        self.tagEdit.setObjectName("tagEdit")
        self.addButton = QtWidgets.QPushButton(AddTag)
        self.addButton.setGeometry(QtCore.QRect(130, 240, 61, 28))
        self.addButton.setObjectName("addButton")
        self.saveButton = QtWidgets.QPushButton(AddTag)
        self.saveButton.setGeometry(QtCore.QRect(200, 240, 61, 28))
        self.saveButton.setObjectName("saveButton")
        self.pathLabel = QtWidgets.QLabel(AddTag)
        self.pathLabel.setGeometry(QtCore.QRect(10, 0, 251, 41))
        self.pathLabel.setTextFormat(QtCore.Qt.RichText)
        self.pathLabel.setScaledContents(False)
        self.pathLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.pathLabel.setWordWrap(True)
        self.pathLabel.setObjectName("pathLabel")

        self.retranslateUi(AddTag)
        QtCore.QMetaObject.connectSlotsByName(AddTag)
        AddTag.setTabOrder(self.tagEdit, self.addButton)
        AddTag.setTabOrder(self.addButton, self.saveButton)
        AddTag.setTabOrder(self.saveButton, self.tagList)

    def retranslateUi(self, AddTag):
        _translate = QtCore.QCoreApplication.translate
        AddTag.setWindowTitle(_translate("AddTag", "添加标签 - File Tagger"))
        self.tagList.headerItem().setText(0, _translate("AddTag", "已有标签:"))
        self.addButton.setText(_translate("AddTag", "添加"))
        self.saveButton.setText(_translate("AddTag", "确认"))
        self.pathLabel.setToolTip(_translate("AddTag", "path"))
        self.pathLabel.setText(_translate("AddTag", "path"))

