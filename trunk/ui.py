# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Sun Dec 16 17:12:19 2007
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(QtCore.QSize(QtCore.QRect(0,0,557,507).size()).expandedTo(Dialog.minimumSizeHint()))
        Dialog.setSizeGripEnabled(True)

        self.vboxlayout = QtGui.QVBoxLayout(Dialog)
        self.vboxlayout.setObjectName("vboxlayout")

        self.frame = QtGui.QFrame(Dialog)
        self.frame.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtGui.QFrame.Raised)
        self.frame.setObjectName("frame")

        self.hboxlayout = QtGui.QHBoxLayout(self.frame)
        self.hboxlayout.setObjectName("hboxlayout")

        self.imgList = QtGui.QListWidget(self.frame)
        self.imgList.setIconSize(QtCore.QSize(150,150))
        self.imgList.setObjectName("imgList")
        self.hboxlayout.addWidget(self.imgList)

        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName("vboxlayout1")

        self.btnAdd = QtGui.QPushButton(self.frame)
        self.btnAdd.setObjectName("btnAdd")
        self.vboxlayout1.addWidget(self.btnAdd)

        self.btnRemove = QtGui.QPushButton(self.frame)
        self.btnRemove.setObjectName("btnRemove")
        self.vboxlayout1.addWidget(self.btnRemove)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.vboxlayout.addWidget(self.frame)

        self.frame_2 = QtGui.QFrame(Dialog)
        self.frame_2.setFrameShape(QtGui.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtGui.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")

        self.vboxlayout2 = QtGui.QVBoxLayout(self.frame_2)
        self.vboxlayout2.setObjectName("vboxlayout2")

        self.tabWidget = QtGui.QTabWidget(self.frame_2)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.tab)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.textBBCode = QtGui.QTextEdit(self.tab)
        self.textBBCode.setObjectName("textBBCode")
        self.hboxlayout1.addWidget(self.textBBCode)
        self.tabWidget.addTab(self.tab,"")
        self.vboxlayout2.addWidget(self.tabWidget)
        self.vboxlayout.addWidget(self.frame_2)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.comboSite = QtGui.QComboBox(Dialog)
        self.comboSite.setObjectName("comboSite")
        self.hboxlayout2.addWidget(self.comboSite)

        self.btnUpload = QtGui.QPushButton(Dialog)
        self.btnUpload.setObjectName("btnUpload")
        self.hboxlayout2.addWidget(self.btnUpload)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.retranslateUi(Dialog)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(QtGui.QApplication.translate("Dialog", "Image uploader", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("Dialog", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRemove.setText(QtGui.QApplication.translate("Dialog", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("Dialog", "BBCode", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpload.setText(QtGui.QApplication.translate("Dialog", "Upload", None, QtGui.QApplication.UnicodeUTF8))

