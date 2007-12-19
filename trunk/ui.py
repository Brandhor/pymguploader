# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ui.ui'
#
# Created: Wed Dec 19 20:22:49 2007
#      by: PyQt4 UI code generator 4.3.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(QtCore.QSize(QtCore.QRect(0,0,555,557).size()).expandedTo(MainWindow.minimumSizeHint()))

        self.centralwidget = QtGui.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.vboxlayout = QtGui.QVBoxLayout(self.centralwidget)
        self.vboxlayout.setObjectName("vboxlayout")

        self.frame = QtGui.QFrame(self.centralwidget)
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
        self.btnAdd.setIcon(QtGui.QIcon(":/new/prefix1/img/add.png"))
        self.btnAdd.setObjectName("btnAdd")
        self.vboxlayout1.addWidget(self.btnAdd)

        self.btnRemove = QtGui.QPushButton(self.frame)
        self.btnRemove.setIcon(QtGui.QIcon(":/new/prefix1/img/delete.png"))
        self.btnRemove.setObjectName("btnRemove")
        self.vboxlayout1.addWidget(self.btnRemove)

        spacerItem = QtGui.QSpacerItem(20,40,QtGui.QSizePolicy.Minimum,QtGui.QSizePolicy.Expanding)
        self.vboxlayout1.addItem(spacerItem)
        self.hboxlayout.addLayout(self.vboxlayout1)
        self.vboxlayout.addWidget(self.frame)

        self.tabWidget = QtGui.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")

        self.tab = QtGui.QWidget()
        self.tab.setObjectName("tab")

        self.hboxlayout1 = QtGui.QHBoxLayout(self.tab)
        self.hboxlayout1.setObjectName("hboxlayout1")

        self.textBBCode = QtGui.QTextEdit(self.tab)
        self.textBBCode.setObjectName("textBBCode")
        self.hboxlayout1.addWidget(self.textBBCode)
        self.tabWidget.addTab(self.tab,"")
        self.vboxlayout.addWidget(self.tabWidget)

        self.hboxlayout2 = QtGui.QHBoxLayout()
        self.hboxlayout2.setObjectName("hboxlayout2")

        self.comboSite = QtGui.QComboBox(self.centralwidget)
        self.comboSite.setObjectName("comboSite")
        self.hboxlayout2.addWidget(self.comboSite)

        self.btnUpload = QtGui.QPushButton(self.centralwidget)
        self.btnUpload.setIcon(QtGui.QIcon(":/new/prefix1/img/upload.png"))
        self.btnUpload.setObjectName("btnUpload")
        self.hboxlayout2.addWidget(self.btnUpload)

        self.btnCancel = QtGui.QPushButton(self.centralwidget)
        self.btnCancel.setIcon(QtGui.QIcon(":/new/prefix1/img/cancel.png"))
        self.btnCancel.setObjectName("btnCancel")
        self.hboxlayout2.addWidget(self.btnCancel)
        self.vboxlayout.addLayout(self.hboxlayout2)

        self.lblTotal = QtGui.QLabel(self.centralwidget)
        self.lblTotal.setObjectName("lblTotal")
        self.vboxlayout.addWidget(self.lblTotal)

        self.pbTotal = QtGui.QProgressBar(self.centralwidget)
        self.pbTotal.setProperty("value",QtCore.QVariant(0))
        self.pbTotal.setObjectName("pbTotal")
        self.vboxlayout.addWidget(self.pbTotal)

        self.lblPartial = QtGui.QLabel(self.centralwidget)
        self.lblPartial.setObjectName("lblPartial")
        self.vboxlayout.addWidget(self.lblPartial)

        self.pbPartial = QtGui.QProgressBar(self.centralwidget)
        self.pbPartial.setProperty("value",QtCore.QVariant(0))
        self.pbPartial.setObjectName("pbPartial")
        self.vboxlayout.addWidget(self.pbPartial)
        MainWindow.setCentralWidget(self.centralwidget)

        self.menubar = QtGui.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0,0,555,21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.statusbar = QtGui.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QtGui.QApplication.translate("MainWindow", "Image Uploader", None, QtGui.QApplication.UnicodeUTF8))
        self.btnAdd.setText(QtGui.QApplication.translate("MainWindow", "Add", None, QtGui.QApplication.UnicodeUTF8))
        self.btnRemove.setText(QtGui.QApplication.translate("MainWindow", "Remove", None, QtGui.QApplication.UnicodeUTF8))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), QtGui.QApplication.translate("MainWindow", "BBCode", None, QtGui.QApplication.UnicodeUTF8))
        self.btnUpload.setText(QtGui.QApplication.translate("MainWindow", "Upload", None, QtGui.QApplication.UnicodeUTF8))
        self.btnCancel.setText(QtGui.QApplication.translate("MainWindow", "Cancel", None, QtGui.QApplication.UnicodeUTF8))

import res_rc
