# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DPU.ui'
#
# Created by: PyQt5 UI code generator 5.12.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1048, 864)
        font = QtGui.QFont()
        font.setPointSize(12)
        MainWindow.setFont(font)
        MainWindow.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))
        MainWindow.setMouseTracking(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.shot = QtWidgets.QSpinBox(self.centralwidget)
        self.shot.setGeometry(QtCore.QRect(10, 10, 91, 31))
        self.shot.setMaximum(999999)
        self.shot.setObjectName("shot")
        self.Warning = QtWidgets.QTextBrowser(self.centralwidget)
        self.Warning.setGeometry(QtCore.QRect(10, 150, 411, 471))
        self.Warning.setObjectName("Warning")
        # add curve layout
        # add shot together
        self.layoutMode = QtWidgets.QComboBox(self.centralwidget)
        self.layoutMode.setGeometry(QtCore.QRect(10, 70, 93, 28))
        self.layoutMode.setObjectName("layoutMode")

        infomation = ["1", "1,1", "111", "1,1+n/2", "cmp"]
        self.layoutMode.addItems(infomation)

        # self.label3.setText(combox.currentText())
        # combox.activated[str].connect(self.zhuangB)
        #


        self.shotTogether = QtWidgets.QPushButton(self.centralwidget)
        self.shotTogether.setGeometry(QtCore.QRect(10, 70, 93, 28))
        self.shotTogether.setObjectName("shotTogether")

        self.shotOK = QtWidgets.QPushButton(self.centralwidget)
        self.shotOK.setGeometry(QtCore.QRect(10, 70, 93, 28))
        self.shotOK.setObjectName("shotOK")
        self.Files = QtWidgets.QListWidget(self.centralwidget)
        self.Files.setGeometry(QtCore.QRect(450, 50, 121, 581))
        self.Files.setObjectName("Files")
        self.Curves = QtWidgets.QListWidget(self.centralwidget)
        self.Curves.setGeometry(QtCore.QRect(600, 50, 121, 581))
        self.Curves.setObjectName("Curves")
        self.Channels = QtWidgets.QListWidget(self.centralwidget)
        self.Channels.setGeometry(QtCore.QRect(750, 50, 121, 581))
        self.Channels.setAutoFillBackground(True)
        self.Channels.setObjectName("Channels")
        self.draw = QtWidgets.QPushButton(self.centralwidget)
        self.draw.setGeometry(QtCore.QRect(10, 100, 93, 28))
        self.draw.setObjectName("draw")
        self.LabelFiles = QtWidgets.QLabel(self.centralwidget)
        self.LabelFiles.setGeometry(QtCore.QRect(470, 20, 72, 15))
        self.LabelFiles.setObjectName("LabelFiles")
        self.LabelCurves = QtWidgets.QLabel(self.centralwidget)
        self.LabelCurves.setGeometry(QtCore.QRect(620, 20, 72, 15))
        self.LabelCurves.setObjectName("LabelCurves")
        self.Browser = QtWidgets.QPushButton(self.centralwidget)
        self.Browser.setGeometry(QtCore.QRect(750, 10, 131, 28))
        self.Browser.setAutoFillBackground(True)
        self.Browser.setObjectName("Browser")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 660, 729, 161))
        self.groupBox.setAutoFillBackground(True)
        self.groupBox.setObjectName("groupBox")
        self.clearAll = QtWidgets.QPushButton(self.centralwidget)
        self.clearAll.setGeometry(QtCore.QRect(110, 100, 93, 28))
        self.clearAll.setObjectName("clearAll")
        self.clearOne = QtWidgets.QPushButton(self.centralwidget)
        self.clearOne.setGeometry(QtCore.QRect(110, 100, 93, 28))
        self.clearOne.setObjectName("clearOne")
        self.xLeft = QtWidgets.QLineEdit(self.centralwidget)
        self.xLeft.setGeometry(QtCore.QRect(100, 10, 91, 31))
        self.xLeft.setObjectName("xLeft")
        self.xLeft.setText('0')
        self.xRight = QtWidgets.QLineEdit(self.centralwidget)
        self.xRight.setGeometry(QtCore.QRect(200, 10, 91, 31))
        self.xRight.setObjectName("xRight")
        self.xRight.setText('10')
        self.freqInterp = QtWidgets.QLineEdit(self.centralwidget)
        self.freqInterp.setGeometry(QtCore.QRect(300, 10, 91, 31))
        self.freqInterp.setObjectName("freqInterp")
        self.freqInterp.setText('0.001')
        self.update = QtWidgets.QPushButton(self.centralwidget)
        self.update.setGeometry(QtCore.QRect(110, 70, 93, 28))
        self.update.setObjectName("update")
        self.chnlPattern = QtWidgets.QLineEdit(self.centralwidget)
        self.chnlPattern.setGeometry(QtCore.QRect(240, 70, 101, 31))
        self.chnlPattern.setPlaceholderText("Search Chnl") # search bar
        self.chnlPattern.setObjectName("chnlPattern")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 1048, 26))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        # Up/down and Sorting
        self.channel = QtWidgets.QPushButton(self.centralwidget)
        self.channel.setGeometry(QtCore.QRect(110, 10, 93, 28))
        self.channel.setObjectName("channel")

        self.up = QtWidgets.QPushButton(self.centralwidget)
        self.up.setGeometry(QtCore.QRect(110, 130, 93, 28))
        self.up.setObjectName("up")

        self.down = QtWidgets.QPushButton(self.centralwidget)
        self.down.setGeometry(QtCore.QRect(200, 130, 93, 28))
        self.down.setObjectName("down")

        self.sort = QtWidgets.QPushButton(self.centralwidget)
        self.sort.setGeometry(QtCore.QRect(200, 160, 93, 28))
        self.sort.setObjectName("Sort")


        # 水平布局

        #      wid = QtGui.QWidget(self)
        # self.setCentralWidget(wid)
        # layout = QtGui.QHBoxLayout()

        layout = QHBoxLayout()
        # 实例化主窗口的QMenuBar对象
        bar = self.menuBar()
        # 向菜单栏中添加新的QMenu对象，父菜单
        file = bar.addMenu('File')
        machine = bar.addMenu('Machine')
        help = bar.addMenu('Help')
        # 向QMenu小控件中添加按钮，子菜单
        file.addAction('setSystemName')
        file.addAction('saveConfig')
        file.addAction('saveData')
        file.addAction('loadData')
        file.addAction('loadConfig')
        file.addAction('drawMode')

        machine.addAction('setMachine')
        machine.addAction('ChnlConfig')
        machine.addAction('scanTree')
        machine.addAction('scanTreeAD')
        machine.addAction('defaultChnl')

        help.addAction('Basics')
        help.addAction('Buttons')
        help.addAction('Drop Down Menu')

        file.triggered[QAction].connect(self.processTrigger)
        machine.triggered[QAction].connect(self.machineTrigger)
        help.triggered[QAction].connect(self.helpTrigger)

        # wid.setLayout(layout)
        self.setLayout(layout)
        self.setWindowTitle('menu例子')

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        self.MainWindow = MainWindow
        self.resizeDP(self.MainWindow)

    def mouseMoveEvent(self, event):
        s = event.pos()
        self.setMouseTracking(True)
        self.Warning.append('X:' + str(s.x()))
        self.Warning.append('Y:' + str(s.y()))

        desktop = QtWidgets.QApplication.desktop()

        Rows = 20
        Cols = 6
        width = desktop.width() * 0.9
        height = desktop.height() * 0.9
        wstep = width / Cols
        hstep = height / Rows
        if s.x() < 2 * wstep and s.y() > 12 * hstep:
            self.resizeDP1(self.MainWindow)

        if s.x() > 4 * wstep and s.y() < 6 * hstep:
            self.resizeDP(self.MainWindow)

    def resizeDP1(self, window):
        desktop = QtWidgets.QApplication.desktop()

        Rows = 20
        Cols = 6
        width = desktop.width() * 0.9
        height = desktop.height() * 0.9
        wstep = width / Cols
        hstep = height / Rows

        w = 0.99 * wstep
        h = 0.94 * hstep

        self.shot.setGeometry(0 * wstep, 0 * h, 0.5 * w, 1 * h)
        self.layoutMode.setGeometry(0 * wstep, 1 * h, 0.5 * w, 1 * h)
        self.shotTogether.setGeometry(0 * wstep, 2 * h, 0.5 * w, 1 * h)

        self.xLeft.setGeometry(0.5 * wstep, 0 * h, 0.5 * w, 1 * h)
        self.shotOK.setGeometry(0.5 * wstep, 1 * h, 0.5 * w, 1 * h)
        self.draw.setGeometry(0.5 * wstep, 2 * h, 0.5 * w, 1 * h)

        # 1.0
        self.xRight.setGeometry(1.0 * wstep, 0 * h, 0.5 * w, 1 * h)
        self.update.setGeometry(1.0 * wstep, 1 * h, 0.5 * w, 1 * h)
        self.chnlPattern.setGeometry(1.0 * wstep, 2 * h, 0.5 * w, 1 * h)

        self.freqInterp.setGeometry(1.5 * wstep, 0 * h, 0.5* w, 1 * h)

        self.clearAll.setGeometry(2.0 * wstep, 0 * h, 0.5 * w, 1 * h)
        self.clearOne.setGeometry(2.5 * wstep, 0 * h, 0.5 * w, 1 * h)
        self.Warning.setGeometry(0.01 * wstep, 3 * h, 2.99 * w, 9.2 * h)

        self.LabelFiles.setGeometry(3 * wstep, 0 * h, 0.99 * w, 1 * h)
        self.LabelCurves.setGeometry(4 * wstep, 0 * h, 0.99 * w, 1 * h)
        self.Browser.setGeometry(5 * wstep, 0 * h, 0.99 * w, 1 * h)
        self.Files.setGeometry(3 * wstep, 1 * h, 0.99 * w, 7.2 * h)
        self.Curves.setGeometry(4 * wstep, 1 * h, 0.99 * w, 7.2 * h)
        self.Channels.setGeometry(5 * wstep, 1 * h, 0.99 * w, 7.2 * h)
        self.groupBox.setGeometry(0.4, 8 * h, 6.03 * w, 12.5 * h)

        # Up/down and Sort
        self.up.setGeometry(2.0 * wstep, 1 * h, 0.5 * w, 1 * h)
        self.channel.setGeometry(2.0 * wstep, 2 * h, 0.5 * w, 1 * h)
        self.down.setGeometry(2.5 * wstep, 1 * h, 0.5 * w, 1 * h)
        self.sort.setGeometry(2.5 * wstep, 2 * h, 0.5 * w, 1 * h)

    def resizeDP(self, window):
        window.move(window.width() * -2, 0)  # 先将窗口放到屏幕外，可避免移动窗口时的闪烁现象。
        desktop = QtWidgets.QApplication.desktop()

        Rows = 20
        Cols = 6
        width = desktop.width() * 0.9
        height = desktop.height() * 0.9
        if width > 2500:
            width = 1800
            height = 1000

        wstep = width / Cols
        hstep = height / Rows


        w = 0.99 * wstep
        h = 0.94 * hstep

        # window.resize(0, 0)
        window.resize(width, height)
        # x = (desktop.width() - window.frameSize().width()) // 2
        # y = (desktop.height() - window.frameSize().height()) // 2
        # window.move(x, y - 30)
        window.move(0, 0)
        window.show()

        self.shot.setGeometry(0 * wstep, 0 * h, 0.5* w, 1 * h)
        self.layoutMode.setGeometry(0 * wstep, 1 * h, 0.5 * w, 1 * h)
        self.shotTogether.setGeometry(0 * wstep, 2 * h, 0.5 * w, 1 * h)

        self.xLeft.setGeometry(0.5 * wstep, 0 * h, 0.5* w, 1 * h)
        self.shotOK.setGeometry(0.5 * wstep, 1 * h, 0.5 * w, 1 * h)
        self.draw.setGeometry(0.5 * wstep, 2 * h, 0.5 * w, 1 * h)

        # 1.0
        self.xRight.setGeometry(1.0 * wstep, 0 * h, 0.5* w, 1 * h)
        self.update.setGeometry(1.0 * wstep, 1 * h, 0.5 * w, 1 * h)
        self.chnlPattern.setGeometry(1.0 * wstep, 2 * h, 0.5 * w, 1 * h)


        self.freqInterp.setGeometry(1.5 * wstep, 0 * h, 0.5* w, 1 * h)

        self.clearAll.setGeometry(2.0 * wstep, 0 * h, 0.5 * w, 1 * h)
        self.clearOne.setGeometry(2.5 * wstep, 0 * h, 0.5 * w, 1 * h)
        self.Warning.setGeometry(0.01 * wstep, 3 * h, 2.99 * w, 9.2 * h)

        self.LabelFiles.setGeometry(3 * wstep, 0 * h, 0.99 * w, 1 * h)
        self.LabelCurves.setGeometry(4 * wstep, 0 * h, 0.99 * w, 1 * h)
        self.Browser.setGeometry(5 * wstep, 0 * h, 0.99 * w, 1 * h)
        self.Files.setGeometry(3 * wstep, 1 * h, 0.99 * w, 19.5 * h)
        self.Curves.setGeometry(4 * wstep, 1 * h, 0.99 * w, 19.5 * h)
        self.Channels.setGeometry(5 * wstep, 1 * h, 0.99 * w, 19.5 * h)
        self.groupBox.setGeometry(0.2, 12 * h, 3 * w, 8.5 * h)

        # Up/down and Sort
        self.up.setGeometry(2.0 * wstep, 1 * h, 0.5 * w, 1 * h)
        self.channel.setGeometry(2.0 * wstep, 2 * h, 0.5 * w, 1 * h)
        self.down.setGeometry(2.5 * wstep, 1 * h, 0.5 * w, 1 * h)
        self.sort.setGeometry(2.5 * wstep, 2 * h, 0.5 * w, 1 * h)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DP by Dr. SONG Xianming"))
        self.shotOK.setText(_translate("MainWindow", "shotOK"))
        self.shotTogether.setText(_translate("MainWindow", "shotTogether"))
        self.draw.setText(_translate("MainWindow", "draw"))
        self.LabelFiles.setText(_translate("MainWindow", "Files"))
        self.LabelCurves.setText(_translate("MainWindow", "Curves"))
        self.Browser.setText(_translate("MainWindow", "Browser"))
        self.groupBox.setTitle(_translate("MainWindow", "GroupBox"))
        self.clearAll.setText(_translate("MainWindow", "clearAll"))
        self.clearOne.setText(_translate("MainWindow", "clearOne"))
        self.update.setText(_translate("MainWindow", "update"))
        self.chnlPattern.setToolTip(_translate("MainWindow", "channel pattern"))

        # Up/down and Sort
        self.up.setText(_translate("MainWindow", "up"))
        self.channel.setText(_translate("MainWindow", "channel"))
        self.down.setText(_translate("MainWindow", "down"))
        self.sort.setText(_translate("MainWindow", "Sort"))
