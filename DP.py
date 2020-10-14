
# "DP by Dr. SONG Xianming"
# 2019.6.6

# from PyQt5.QtWidgets import QFileDialog, QApplication, QWidget, QLineEdit, \
#     QInputDialog, QGridLayout, QLabel, QPushButton, QFrame
import scipy.io as sio
import sxm
import InfChnl
import os
import re
import math
import DPI
import numpy as np
import pyqtgraph as pg

import sys
from PyQt5 import QtWidgets, QtCore, QtGui
# from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QMainWindow,QMessageBox
from PyQt5.QtWidgets import *
from PyQt5.QtGui import QPalette, QFont
from PyQt5.QtCore import *
from DPU import Ui_MainWindow
# figure
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
# from matplotlib.backends.backend_qt5 import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use("Qt5Agg")  # 声明使用QT5

if True:
    # global definition
    setMachineMode = 0
    setTreeMode = 0
    machineName = 'HL2A'
    treeNames = []

    showInfMode = 0
    oscilloscopeMode = 0
    mouseDown = 0
    mouseMove = 0
    myWidth = 0
    myHeight = 0
    myDPI = 0
    myStart = 0
    myEnd = 10
    defaultPos = [0.05, 0.1, 0.9, 0.75]
    lineWidth=2
    fontSize=18
    progress = 0
    total = 0
    tickNumber = 3
    drawMode = 1  # 0=matlab for publishing, 1=pyqtgraph for analysing
    isDrawConfigReady=0  #set to 1 before drawing


    trajectoryX = []
    trajectoryY = []
    trajectoryXData = []
    mouseDownPos=[]

    hAxes = []
    hVBs = []
    hPIs = []
    ind=0  # the axes number selected by mouse

    hLines = []
    myBox = []
    myText = []

    hLine1 = []
    vLine1 = []
    hLine2 = []
    vLine2 = []
    gWarning = []

class selectChnl(QWidget):
    signalChnl = pyqtSignal(list)  # send back the ChnlName to mainwindow

    def __init__(self, Chnl):
        super(selectChnl, self).__init__()

        self.Chnl=Chnl
        self.initUi()

    def initUi(self):
        self.label={}
        self.setWindowTitle("select the channel")
        self.setGeometry(400, 400, 300, 260)

        mainLayout = QGridLayout()

        sLabel = ['num',  'all', 'ChnlName']
        sType = ['QLabel',  'QCheckBox', 'QLabel']
        sTypeChnl = ['QLabel',  'QCheckBox', 'QLineEdit']

        Chnl = self.Chnl

        for i in range(len(sLabel)):
            exec(r'self.label[i]=' + sType[i] + '("' + sLabel[i] + '")')

            # self.label[i].setFrameStyle(QFrame.Panel | QFrame.Sunken)

            mainLayout.addWidget(self.label[i], 0, i)
            cmd = 'self.' + sLabel[i] + '={}'
            exec(cmd)

        self.label[1].stateChanged.connect(self.changecb1)

        for j in range(len(Chnl)):
            cmd = 'self.' + sLabel[0] + '[j]=' + sTypeChnl[0] + '("' + str(j+1) + '")'
            exec(cmd)

            cmd = 'mainLayout.addWidget(self.' + sLabel[0] + '[j], j+1, 0)'
            exec(cmd)

            cmd = 'self.' + sLabel[1] + '[j]=' + sTypeChnl[1] + '("' + str(j+1) + '")'
            exec(cmd)
            cmd = 'mainLayout.addWidget(self.' + sLabel[1] + '[j], j+1, 1)'
            exec(cmd)

            cmd = 'self.' + sLabel[1] + '[j].stateChanged.connect(self.changecb2)'
            exec(cmd)

            cmd = 'self.' + sLabel[2] + '[j]=' + sTypeChnl[2] + '("' + Chnl[j] + '")'
            exec(cmd)

            cmd = 'mainLayout.addWidget(self.' + sLabel[2] + '[j], j+1, 2)'
            exec(cmd)

        ButtonOK = QPushButton("OK")
        cmd = 'mainLayout.addWidget(ButtonOK, len(Chnl)+1, 0)'
        exec(cmd)

        # all selected
        for i in range(len(self.all)):
            self.all[i].setChecked(True)

        self.label[1].setChecked(True)
        ButtonOK.clicked.connect(self.setOK)

        self.setLayout(mainLayout)

    def setOK(self):
        newChnlName=[]

        for i in range(len(self.all)):
            if self.all[i].isChecked():
                chnl=self.ChnlName[i].text()
                newChnlName.append(chnl)

        self.signalChnl.emit(newChnlName)
        self.close()

    def changecb1(self):
        if self.label[1].checkState() == Qt.Checked:
            for i in range(len(self.all)):
                self.all[i].setChecked(True)
        elif self.label[1].checkState() == Qt.Unchecked:
            for i in range(len(self.all)):
                self.all[i].setChecked(False)

    def changecb2(self):
        sum=0

        for i in range(len(self.all)):
            sum += int(self.all[i].isChecked())

        if sum==len(self.all):
            self.label[1].setTristate(False)
            self.label[1].setCheckState(Qt.Checked)
        elif sum>0:
            self.label[1].setTristate()
            self.label[1].setCheckState(Qt.PartiallyChecked)
        else:
            self.label[1].setTristate(False)
            self.label[1].setCheckState(Qt.Unchecked)

class modifyConfig(QWidget):
    # myCurveData = CurveData('songxm')
    signalCurve = pyqtSignal(dict)  # send back the curveData to mainwindow

    def __init__(self, myData):
        super(modifyConfig, self).__init__()
        self.CurveData=myData
        sLabel = ['Num', 'Loc', 'Right', 'Color', 'Marker', 'LineStyle', 'FraNum', 'XOffset', 'YOffset',\
                  'Factor', 'Unit', 'Stairs', 'ChnlName', 'Min', 'Max']
        sType = ['QLabel',  'QLineEdit', 'QLineEdit', 'QLineEdit', 'QLineEdit', 'QLineEdit', 'QLineEdit',\
                 'QLineEdit', 'QLineEdit', 'QLineEdit',
                 'QLineEdit', 'QLineEdit', 'QLineEdit', 'QLineEdit', 'QLineEdit', 'QLineEdit']

        self.sLabel = sLabel
        self.sType = sType
        self.initUi()

    def initUi(self):
        Curves = self.CurveData
        sLabel = self.sLabel
        sType = self.sType


        self.label={}
        self.setWindowTitle("Modify the channel information")
        self.setGeometry(400, 400, 300, 260)

        mainLayout = QGridLayout()



        # n1 = myTree.getNode(r"\{}".format(channelName))

        for i in range(len(sLabel)):
            self.label[i]=QLabel(sLabel[i])
            self.label[i].setFrameStyle(QFrame.Panel | QFrame.Sunken)
            mainLayout.addWidget(self.label[i], 0, i)
            cmd = 'self.' + sLabel[i] + '={}'
            exec(cmd)

        for j in range(len(Curves.ChnlName)):
            for i in range(len(sLabel)):
                # Num[j]=QLabel(str(j))
                cmd = 'self.' + sLabel[i] + '[j]=' + sType[i] + '(str(Curves.' + sLabel[i] + '[j]))'
                exec(cmd)
                cmd = 'mainLayout.addWidget(self.' + sLabel[i] + '[j], j+1, i)'
                exec(cmd)

        ButtonOK = QPushButton("OK")
        cmd = 'mainLayout.addWidget(ButtonOK, len(Curves.ChnlName)+1, 0)'
        exec(cmd)
        ButtonOK.clicked.connect(self.setOK)

        self.setLayout(mainLayout)

    def setOK(self):
        Curves = self.CurveData
        sLabel = self.sLabel

        for j in range(len(Curves.ChnlName)):
            for i in range(len(sLabel)):
                # Num[j]=QLabel(str(j))
                # cmd = 'self.' + sLabel[i] + '[j]=' + sType[i] + '(str(Curves.' + sLabel[i] + '[j]))'
                cmd= 'Curves.' + sLabel[i] + '[j]=self.' + sLabel[i] + '[j].text()'

                exec(cmd)
        dictCurves={}
        for i in range(len(sLabel)):
            cmd = 'dictCurves["' + sLabel[i] + '"]=Curves.' + sLabel[i]
            exec(cmd)

        pass

        self.signalCurve.emit(dictCurves)
        self.close()



# the event for the DP
def on_key_press(event):
    global trajectoryX, trajectoryY, mouseDown, mouseMove, showInfMode
    global oscilloscopeMode
    try:
        if event.key =='f1':  # Qt.Key_F1:
            mouseMove=0

        elif event.key == 'f5':
            oscilloscopeMode=1

        elif event.key == 'escape':
            oscilloscopeMode=0
            plt.setp(hLine1, 'xdata', [0, 0], 'ydata', [0, 0])
            plt.setp(vLine1, 'xdata', [0, 0], 'ydata', [0, 0])
            plt.setp(hLine2, 'xdata', [0, 0], 'ydata', [0, 0])
            plt.setp(vLine2, 'xdata', [0, 0], 'ydata', [0, 0])
            plt.setp(myText, 'x', 0, 'y', 0, 'text', '')

        elif event.key in ['u', 'U']:
            for i in range(len(hAxes)):
                axes = hAxes[i]
                line = hLines[i]
                myXLim = axes.get_xlim()

                x=line[0].get_xdata()
                y=line[0].get_ydata()
                # make sure the span is right
                if myXLim[0] < min(x):
                    myX1 = min(x)
                else:
                    myX1 = myXLim[0]

                if myXLim[1] > max(x):
                    myX2 = max(x)
                else:
                    myX2 = myXLim[1]

                myY = sxm.getYData(x, y, [myX1, myX2])

                newYLim, myTickY, myTickYLabel=sxm.MyYTick([min(myY), max(myY)], 3, 2, 0)
                axes.set_ylim(newYLim)
                axes.set_yticks(myTickY)
                axes.set_yticklabels(myTickYLabel)
                # x Tick
                myTickX = np.arange(myX1, myX2, (myX2-myX1)/10)
                axes.set_xticks(myTickX)


                #
                # myTickXLabel = []
                # for ix in range(len(myTickX)):
                #         cmd = "myTickXLabel.append(str(myTickX[ix]))"
                #         exec(cmd)
                #
                # axes.set_xticklabels(myTickXLabel)



        elif event.key is 'shift':
            showInfMode = 1


    except:
        gWarning.append('on_key_press' + ' or something wrong')
    else:
        gWarning.append('on_key_press' + ' is OK')


def motion_notify(event):
    global trajectoryX, trajectoryY,trajectoryXData,  mouseDown, mouseMove
    global myBox, myWidth, myHeight, myDPI, oscilloscopeMode, hLine1, vLine1, hLine2, vLine2, myText
    try:
        if mouseMove==1:
            debug=1
            mouseMove=0

        if mouseDown==1:
            trajectoryX.append(event.x)
            trajectoryY.append(event.y)
            trajectoryXData.append(event.xdata)

        if len(trajectoryX) > 1:
            if mouseDown == 1:
                myBox.patch.set_color('r')
                pos=[trajectoryX[0]/(myWidth*myDPI), trajectoryY[0]/(myHeight*myDPI), (event.x-trajectoryX[0])/(myWidth*myDPI), (event.y-trajectoryY[0])/(myHeight*myDPI)]
                myBox.set_position(pos, which='both')
        else:

            if oscilloscopeMode==1:
                bools_list = list(map(lambda x: x.contains_point((event.x, event.y)), hAxes))

                if sum(bools_list)==0:
                    myBox.set_position([1,1,0,0])
                else:
                    ind = bools_list.index(True)

                    currentAxes = hAxes[ind]
                    myXLim=currentAxes.get_xlim()
                    myYLim=currentAxes.get_ylim()

                    plt.sca(myBox)
                    myBox.patch.set_color('none')
                    myBox.set_xlim(myXLim)
                    myBox.set_ylim(myYLim)
                    myBox.set_position(currentAxes.get_position())

                    plt.setp(hLine2, 'xdata',[myXLim[0],myXLim[1]],'ydata',[event.ydata,event.ydata])
                    plt.setp(vLine2, 'xdata',[event.xdata,event.xdata],'ydata',[myYLim[0],myYLim[1]])

                    x1=vLine1[0].get_xdata()[0]
                    y1=hLine1[0].get_ydata()[0]

                    mystr ='X=' + '{:.2f}'.format(event.xdata) + '\n y=' + '{:.2f}'.format(event.ydata) + \
                           '\n dx=' + '{:.2f}'.format(event.xdata-x1) + '\n dy=' + '{:.2f}'.format(event.ydata-y1)

                    plt.setp(myText, 'x',event.xdata,'y',event.ydata,'text', mystr)
            else:
                    myBox.set_position([1, 1, 0, 0])

        event.canvas.draw()

    except:
        gWarning.append('motion_notify' + ' or something wrong')
    else:
        # gWarning.append('motion_notify' + ' is OK')
        pass



def on_button_press(event):
    global trajectoryX, trajectoryY, trajectoryXData, mouseDown, mouseMove,myBox
    global oscilloscopeMode, hLine1, vLine1, hLine2, vLine2
    global gWarning

    try:
        mouseDown=1
        trajectoryX=[]
        trajectoryY=[]
        trajectoryXData=[]

        if oscilloscopeMode==1:

            bools_list = list(map(lambda x: x.contains_point((event.x, event.y)), hAxes))
            ind = bools_list.index(True)
            currentAxes = hAxes[ind]
            myXLim=currentAxes.get_xlim()
            myYLim=currentAxes.get_ylim()

            plt.sca(myBox)
            myBox.set_xlim(myXLim)
            myBox.set_ylim(myYLim)
            myBox.set_position(currentAxes.get_position())

            plt.setp(hLine1, 'xdata',[myXLim[0],myXLim[1]],'ydata',[event.ydata,event.ydata])
            plt.setp(vLine1, 'xdata',[event.xdata,event.xdata],'ydata',[myYLim[0],myYLim[1]])

        elif oscilloscopeMode==0:
            myBox.set_position([0,0,0,0])

        event.canvas.draw()

    except:
        gWarning.append('on_button_press' + ' or something wrong')
    else:
        gWarning.append('on_button_press' + ' is OK')

def on_button_release(event):
    global trajectoryX, trajectoryY,trajectoryXData,  mouseDown, mouseMove
    global hAxes, myBox, oscilloscopeMode
    global myWidth, myHeight, myDPI, gWarning
    try:
        mouseDown=0
        type=getGesture(trajectoryX, trajectoryY)

        # 11 down
        # 12 up
        # 13 left
        # 14 right

        if type in [5, 9, 14]:
            plt.sca(hAxes[0])
            plt.xlim(trajectoryXData[0], trajectoryXData[-1])
            event.key='u'
            on_key_press(event)

        elif type in [1, 10, 13]:
            plt.sca(hAxes[0])
            plt.xlim(myStart, myEnd)
            event.key='u'
            on_key_press(event)

        elif type is 11:
            # initialize the size

            plt.subplots_adjust(left=defaultPos[0], right=defaultPos[0]+defaultPos[2], bottom=defaultPos[1], top=defaultPos[1]+defaultPos[3], wspace=0.0, hspace=0.0)
            # plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.85, wspace=0.0, hspace=0.0)
            for ha in hAxes:
                plt.sca(ha)
                plt.setp(ha.get_xticklabels(), visible=False)

            plt.setp(ha.get_xticklabels(), visible=True)

        elif type is 12:  # only one axis
            bools_list = list(map(lambda x: x.contains_point((event.x, event.y)), hAxes))
            ind = bools_list.index(True)
            currentAxes= hAxes[ind]

            for ha in hAxes:
                pos = [0, 0, 0, 0]
                ha.set_position(pos, which='both')

            pos=defaultPos
            currentAxes.set_position(pos, which='both')
            plt.setp(currentAxes.get_xticklabels(), visible=True)
            event.key='u'
            on_key_press(event)


        # hide the box
        if oscilloscopeMode ==0:
            pos=[0, 0, 0, 0]
            myBox.set_position(pos, which='both')

        event.canvas.draw()

    except:
        gWarning.append('on_button_release' + ' or something wrong')
    else:
        gWarning.append('on_button_release' + ' is OK')


def getGesture(trajectoryPointX, trajectoryPointY):
    type = 0
    # definition
    # 0 no trajectory
    # 1 first quadrant, anti - clockwise
    # 2 second quadrant, anti - clockwise
    # 3 third quadrant, anti - clockwise
    # 4 fourth quadrant, anti - clockwise

    # 5 first quadrant, clockwise
    # 6 second quadrant, clockwise
    # 7 third quadrant, clockwise
    # 8 fourth quadrant, clockwise

    # 9 zoom in = from lefttop to rightbottom
    # 10 zoom out = from rightbottom to lefttop

    # 11 down
    # 12 up
    # 13 left
    # 14 right

    # 15 = from righttop to leftbottom
    # 16 = from lefttop to rightbottom

    try:

        if len(trajectoryPointX) == 0:
            type = 0
            return type

        X = np.array(trajectoryPointX, dtype=np.float32)
        Y = np.array(trajectoryPointY, dtype=np.float32)
        maxX = max(X)
        minX = min(X)
        midX = (maxX + minX) / 2
        delX = maxX - minX

        maxY = max(Y)
        minY = min(Y)
        midY = (maxY + minY) / 2
        delY = maxY - minY

        aspectRatio = delX / (delY + 0.05)

        if aspectRatio < 0.35:  # updown
            if Y[0] < Y[-1]:
                type = 11  # down= restore
            else:  # Y[0] < Y[-1]
                type = 12  # up=zoom in

        elif aspectRatio < 4:  # square
            # find the relation coef

            N=len(X)
            sumX=sum(X)
            sumY=sum(Y)
            sumXY=sum(X*Y)
            sumXX=sum(X*X)
            sumYY=sum(Y*Y)

            r = (N*sumXY-sumX*sumY)*(N*sumXY-sumX*sumY)/((N*sumXX-sumX*sumX)*(N*sumYY-sumY*sumY))


            # model = linear_model.LinearRegression()
            # model.fit(X, Y)
            # b = model.intercept_  # 截距
            # r = model.coef_  # 线性模型的系数
            # k = model.predict([[12]])
            #
            # # [r, k, b] = regression(X, Y)

            if abs(r) > 0.8:  # linear
                if (X[0] < X[-1]) and (Y[0] > Y[-1]):
                    type = 9  # 9  zoom in =  from lefttop to rightbottom
                elif (X[0] > X[-1]) and (Y[0] < Y[-1]):
                    type = 10  # 10   zoom  out =  from rightbottom to lefttop
                elif (X[0] > X[-1]) and (Y[0] > Y[-1]):
                    type = 15  # 15 =  from righttop to leftbottom
                elif (X[0] < X[-1]) and (Y[0] < Y[-1]):
                    type = 16  # 16 =  from leftbottom to righttop
                else:
                    type = 0

            else:  # not linear
                N1 = sum((X > midX) & (Y > midY))  # first - quadrant
                N2 = sum((X < midX) & (Y > midY))  # second - quadrant
                N3 = sum((X < midX) & (Y < midY))  # third - quadrant
                N4 = sum((X > midX) & (Y < midY))  # fourth - quadrant
                Ns = [N3, N4, N1, N2]

                # [Nmin, index] = min(Ns)  # where is less
                Nmin = min(Ns)  # where is less
                offset = 4

                if Nmin is N3:  # third  less
                    index = 1
                    if X[0] > X[-1]:
                        type = index  # acw  first - quadrant
                    else:
                        type = offset + index  # cw  first - quadrant

                elif Nmin is N4:
                    index = 2
                    if X[0] > X[-1]:
                        type = index  # acw    second - quadrant
                    else:
                        type = offset + index;  # cw  second - quadrant

                elif Nmin is N1:
                    index = 3

                    if X[0] < X[-1]:
                        type = index  # acw  third - quadrant
                    else:
                        type = offset + index  # cw third - quadrant

                elif Nmin is N2:
                    index = 4
                    if X[0] < X[-1]:
                        type = index  # acw  fourth - quadrant
                    else:
                        type = offset + index  # cw  fourth - quadrant

        elif aspectRatio > 5:  # leftright
            if X[0] > X[-1]:
                type = 13  # left
            else:  # X[0] < X[-1]
                type = 14  # right


    except:
        gWarning.append('getGesture' + ' or something wrong')
    else:
        gWarning.append('getGesture' + ' is OK')

    return type


# the event for the DP

def on_key_presspg(event):
    global trajectoryX, trajectoryY, mouseDown, mouseMove, showInfMode
    global myBox, myWidth, myHeight, myDPI, oscilloscopeMode, hLine1, vLine1, hLine2, vLine2, myText

    try:
        if event.key() == Qt.Key_F5:
            oscilloscopeMode=1

        elif event.key() == Qt.Key_Escape:
            oscilloscopeMode=0
            hLine1.hide()
            vLine1.hide()
            hLine2.hide()
            vLine2.hide()
            myText.hide()
            myBox.hide()

        elif event.text() in ['u', 'U']:
            for i in range(len(hAxes)):
                axes = hAxes[i]
                line = hLines[i]
                myXLim = axes.get_xlim()

                x=line[0].get_xdata()
                y=line[0].get_ydata()
                # make sure the span is right
                if myXLim[0] < min(x):
                    myX1 = min(x)
                else:
                    myX1 = myXLim[0]

                if myXLim[1] > max(x):
                    myX2 = max(x)
                else:
                    myX2 = myXLim[1]

                myY = sxm.getYData(x, y, [myX1, myX2])

                newYLim, myTickY, myTickYLabel=sxm.MyYTick([min(myY), max(myY)], 3, 2, 0)
                axes.set_ylim(newYLim)
                axes.set_yticks(myTickY)
                axes.set_yticklabels(myTickYLabel)
                # x Tick
                myTickX = np.arange(myX1, myX2, (myX2-myX1)/10)
                axes.set_xticks(myTickX)
                #
                # myTickXLabel = []
                # for ix in range(len(myTickX)):
                #         cmd = "myTickXLabel.append(str(myTickX[ix]))"
                #         exec(cmd)
                #
                # axes.set_xticklabels(myTickXLabel)



        elif event.key() == Qt.Key_Shift:
            showInfMode = 1


    except:
        gWarning.append('on_key_press' + ' or something wrong')
    else:
        gWarning.append('on_key_press' + ' is OK')

def motion_notifypg(event):
    global trajectoryX, trajectoryY,  mouseDown, mouseMove, mouseDownPos
    global ind
    global myBox, myWidth, myHeight, myDPI, oscilloscopeMode, hLine1, vLine1, hLine2, vLine2, myText
    try:

        if mouseDown==1:
            trajectoryX.append(event.x())
            trajectoryY.append(event.y())

        if len(trajectoryX) > 1:
            if mouseDown == 1:
                myRect =QtCore.QRectF(min(trajectoryX[0],event.x()), min(trajectoryY[0],event.y()), abs(event.x()-trajectoryX[0]), abs(event.y()-trajectoryY[0]))
                myBox.setRect(myRect)
                myBox.show()

        else:

            if oscilloscopeMode==1:
                bools_list = list(map(lambda x: x.contains(x.mapFromScene(event)), hVBs))
                # bools_list = list(map(lambda x: x.contains(x.mapFromScene(event.pos())), hVBs))

                if sum(bools_list)==0:
                    myRect = QtCore.QRectF(0, 0, 0, 0)
                    myBox.setRect(myRect)
                else:

                    ind = bools_list.index(True)
                    myRect = myBox.scene().sceneRect()

                    hLine2.show()
                    vLine2.show()
                    hLine2.setLine(myRect.left(), event.y(), myRect.right(), event.y())
                    vLine2.setLine(event.x(), myRect.top(), event.x(), myRect.bottom())

                    pos=hVBs[ind].mapToView(hVBs[ind].mapFromScene(event))
                    oldPos=hVBs[ind].mapToView(hVBs[ind].mapFromScene(mouseDownPos))
                    x1=pos.x()
                    y1=pos.y()
                    # pos=hVBs[ind].mapToView(hPIs[ind].mapToItem(hVBs[ind],event.pos()-QtCore.QPoint(28,13)))
                    # oldPos=hVBs[ind].mapToView(hPIs[ind].mapToItem(hVBs[ind], mouseDownPos-QtCore.QPoint(28,13)))
                    # x1=pos.x()
                    # y1=pos.y()

                    mystr ='X=' + '{:.2f}'.format(x1) + '\n y=' + '{:.2f}'.format(y1) + \
                           '\n dx=' + '{:.2f}'.format(oldPos.x()-x1) + '\n dy=' + '{:.2f}'.format(oldPos.y()-y1)


                    myText.setHtml(mystr)
                    myQPoint=QtCore.QPointF(event.x(), event.y())
                    myText.setPos(myQPoint)
            else:
                pass
                    # myBox.setPos(10000,0)

    except:
        gWarning.append('motion_notify' + ' or something wrong')
    else:

        # myBox.scene().update(myBox.scene().sceneRect())
        # gWarning.append('motion_notify' + ' is OK')
        pass

def on_button_presspg(event):
    global trajectoryX, trajectoryY, mouseDown, mouseMove, myBox, mouseDownPos
    global oscilloscopeMode, hLine1, vLine1, hLine2, vLine2
    global gWarning

    try:
        mouseDown=1
        mouseDownPos = event.pos()

        trajectoryX=[]
        trajectoryY=[]

        if oscilloscopeMode==1:
            myRect = myBox.scene().sceneRect()
            hLine1.show()
            vLine1.show()
            hLine2.show()
            vLine2.show()
            myText.show()

            hLine1.setLine(myRect.left(),event.y(),myRect.right(),event.y())
            vLine1.setLine(event.x(),myRect.top(),event.x(),myRect.bottom())



    except:
        gWarning.append('on_button_press' + ' or something wrong')
    else:

        # myBox.scene().update(myBox.scene().sceneRect())
        gWarning.append('on_button_press' + ' is OK')

def updateCurves(event, *args):
    global trajectoryX, trajectoryY, mouseDown, mouseMove, posStart, pos
    global ind, hAxes, hVBs, hPIs, myBox, oscilloscopeMode

    # set the mouse position for use. one is the button press down position place, the other is the release position
    posStart = hVBs[ind].mapToView(hVBs[ind].mapFromScene(mouseDownPos))
    pos = hVBs[ind].mapToView(hVBs[ind].mapFromScene(event.pos()))

    if len(args) == 1:
        myXlim=args[0]
    elif len(args) == 0:
        ind1 = 0
        myXlim = [min(posStart.x(), pos.x()), max(posStart.x(), pos.x())]

    hVBs[ind].setXRange(myXlim[0], myXlim[1], padding=0.0, update=True)

    for i in range(len(hPIs)):
        xData = hPIs[i].dataItems[0].xData
        yData = hPIs[i].dataItems[0].yData

        myYspan = sxm.getYData(xData, yData, myXlim)
        yLim = [min(myYspan), max(myYspan)]

        vb = hPIs[i].vb
        myScale = hPIs[i].getAxis('left')

        newYLim, myTickY, myTickYLabel = sxm.MyYTick(yLim, tickNumber, 1, 0)
        vb.setYRange(newYLim[0], newYLim[1], padding=0.0, update=True)
        Ticks = []
        for ii in range(len(myTickY)):
            Ticks.append((myTickY[ii], myTickYLabel[ii]))

        myScale.setTicks([Ticks])

    # # more detail by selecting in box
    # bools_listOld = list(map(lambda x: x.contains(x.mapFromScene(mouseDownPos)), hVBs))
    # # bools_listOld = list(map(lambda x: x.contains(x.mapFromScene(QtCore.QPoint(trajectoryX[0], trajectoryY[0]))), hVBs))
    # indOld = bools_listOld.index(True)
    # if ind == indOld:
    #     yLim = [min(posStart.y(), pos.y()), max(posStart.y(), pos.y())]
    #     newYLim, myTickY, myTickYLabel = sxm.MyYTick(yLim, tickNumber, 1, 0)
    #     hVBs[ind].setYRange(newYLim[0], newYLim[1], padding=0.0, update=True)
    #     Ticks = []
    #     for ii in range(len(myTickY)):
    #         Ticks.append((myTickY[ii], myTickYLabel[ii]))
    #
    #     myScale = hPIs[ind].getAxis('left')
    #     myScale.setTicks([Ticks])


def on_button_releasepg(event):
    global trajectoryX, trajectoryY, mouseDown, mouseMove
    global ind, hAxes, hVBs, hPIs, myBox, oscilloscopeMode
    global myWidth, myHeight, myDPI, gWarning
    try:
        mouseDown=0

        type=getGesture(trajectoryX, trajectoryY)
        # find the axis that the mouse stay at this moment
        bools_list = list(map(lambda x: x.contains(x.mapFromScene(event.pos())), hVBs))
        ind = bools_list.index(True)

        # hide the box
        myBox.hide()


        # type = 12

        # 11 down
        # 12 up
        # 13 left
        # 14 right



        # zoom in
        if type in [5, 9, 14, 16]:
            updateCurves(event)

            # bools_listOld = list(map(lambda x: x.contains(x.mapFromScene(QtCore.QPoint(trajectoryX[0], trajectoryY[0]))), hVBs))
            # indOld = bools_listOld.index(True)
            # if ind==indOld:
            #     yLim = [min(posStart.y(), pos.y()), max(posStart.y(), pos.y())]
            #     newYLim, myTickY, myTickYLabel=sxm.MyYTick(yLim, tickNumber, 1, 0)
            #     hVBs[ind].setYRange(newYLim[0], newYLim[1], padding=0.0, update=True)
            #     Ticks=[]
            #     for ii in range(len(myTickY)):
            #
            #         Ticks.append((myTickY[ii],myTickYLabel[ii]))
            #
            #     myScale = hPIs[ind].getAxis('left')
            #     myScale.setTicks([Ticks])

        elif type in [1, 10, 13,15]:
            # hVBs[ind].setXRange(myStart, myEnd, padding=0.0, update=True)
            updateCurves(event,[myStart, myEnd])




        elif type is 11: # to many axis
            # initialize the size
            for ha in hPIs:
                ha.show()

            myScaleL = hPIs[ind].getAxis('bottom')
            myScaleL.setStyle(showValues=False)
            myScaleL = hPIs[-1].getAxis('bottom')
            myScaleL.setStyle(showValues=True)

        elif type is 12:  # only one axis
            #  #%% the size is controlled by show and hide
            # myRect=hVBs[ind].screenGeometry()
            # myPos=hVBs[ind].pos()
            # myRectAxis=hAxes[ind].geometry()

            # for ha in hVBs:
            #     ha.setGeometry(0,0,0,0)
            # for ha in hAxes:
            #     ha.setGeometry(0,0,0,0)
            for ha in hPIs:
                ha.hide()

            hPIs[ind].show()
            # myRectAll = hVBs[ind].scene().sceneRect()
            #
            # hVBs[ind].setGeometry(myPos.x(), myRectAll.top(), myRect.width(), myRect.height()*len(hAxes))
            # hAxes[ind].setGeometry(myRectAxis.left(), myRectAll.top(), myRectAxis.width(), myRect.height()*len(hAxes))
            myScaleL = hPIs[ind].getAxis('bottom')
            myScaleL.setStyle(showValues=True)



    except:
        gWarning.append('on_button_release' + ' or something wrong')
    else:
        gWarning.append('on_button_release' + ' is OK')


# to store the data for drawing the curves, need to update
class CurveData:
    def __init__(self, author):
        self.author = author
        # list type
        self.Num = []
        self.Loc = []
        self.Right=[]  # left

        self.X = []
        self.Y = []
        self.Min=[]  # left
        self.Max=[]  # right
        self.Label=[]  # for display channel
        self.Unit=[]
        self.ChnlName=[]  # for update channel
        self.Factor=[]
        self.XOffset=[]
        self.YOffset=[]
        self.Color=[]
        self.Marker=[]
        self.LineStyle=[]
        self.Stairs=[]
        self.FraNum=[]
    def remove(self,index):
        del self.Num[index]
        del self.Loc[index]
        del self.Right[index]  # left

        del self.X[index]
        del self.Y[index]
        del self.Min[index]  # left
        del self.Max[index]  # right
        del self.Label[index]  # for display channel
        del self.Unit[index]
        del self.ChnlName[index]  # for update channel
        del self.Factor[index]
        del self.XOffset[index]
        del self.YOffset[index]
        del self.Color[index]
        del self.Marker[index]
        del self.LineStyle[index]
        del self.Stairs[index]
        del self.FraNum[index]



class MyFigure(FigureCanvas):
    def __init__(self,width=3, height=3, dpi=100):  # 第一步：创建一个创建Figure
        self.fig = Figure(figsize=(width, height), dpi=dpi)  # 第二步：在父类中激活Figure窗口
        super(MyFigure,self).__init__(self.fig)  # 此句必不可少，否则不能显示图形 #第三步：创建一个子图，用于绘制图形用，111表示子图编号，如matlab的subplot(1,1,1)
        self.axes = self.fig.add_subplot(111)  # 第四步：就是画图，【可以在此类中画，也可以在其它类中画】


class showProgress(QWidget):

    def __init__(self):
        super(showProgress, self).__init__()
        self.initUi()

    def initUi(self):

        self.setWindowTitle("Progress")
        self.progressBar = QProgressBar(self)
        self.setGeometry(600, 600, 300, 75)

        mainLayout = QGridLayout()
        mainLayout.addWidget(self.progressBar, 0, 1)

        self.setLayout(mainLayout)

    def receiveProgress(self, prog, tot):

        self.progressBar.setMaximum(tot)
        self.progressBar.setMinimum(0)
        self.progressBar.setValue(prog)

        if prog == total:
            self.hide()


class mwindow(QtWidgets.QMainWindow, Ui_MainWindow):

    signalProgress = pyqtSignal(int, int)

    def __init__(self):
        super(mwindow, self).__init__()
        global gWarning
        global myDPI, myWidth, myHeight
        global showInfMode
        global setMachineMode, setTreeMode
        global machineName, treeNames
        # self.hD = []
        # self.hF = []
        # self.mw = []
        # self.gv = []
        # self.l = []


        # the mode is used to control the data source, 1=local,0=server
        if len(sys.argv)>1:
            self.mode = int(sys.argv[1])
        else:
            self.mode = 2


        desktop = QtWidgets.QApplication.desktop()

        myDPI=100
        myWidth=math.floor(desktop.width()*0.9/myDPI)
        myHeight=math.floor(desktop.height()*0.85/myDPI)

        self.setupUi(self)
        self.initDP()
        self.view2Struct()
        self.browserMode = 0
        self.defaultChnl = ''
        # self.defaultChnlSaveLoad()  # load

        gWarning=self.Warning
        self.Browser.setAutoFillBackground(True)

        self.Browser.setAutoFillBackground(True)
        self.Browser.setStyleSheet('background-color:green')
        self.Browser.setStyleSheet('Color:red')
        self.Browser.setStyleSheet("QPushButton:hover{color:blue}")
        self.Browser.setFont(QFont("宋体",20, QFont.Bold))
        self.shotOK.setFont(QFont("宋体",20, QFont.Bold))
        self.update.setFont(QFont("宋体",20, QFont.Bold))
        self.draw.setFont(QFont("宋体",20, QFont.Bold))

        self.Curves.setAlternatingRowColors(True)
        self.Curves.setStyleSheet("QListWidget:hover{color:red}")

        self.Files.setAlternatingRowColors(True)
        self.Channels.setAlternatingRowColors(True)

        p1 = QPalette()
        p1.setColor(QPalette.Window, Qt.red)
        p1.setColor(QPalette.AlternateBase, Qt.cyan)
        self.Curves.setPalette(p1)
        self.Files.setPalette(p1)
        self.Channels.setPalette(p1)

        # self.button.setStyleSheet("QPushButton{color:black}"
        #                           "QPushButton:hover{color:red}"
        #                           "QPushButton{background-color:rgb(78,255,255)}"
        #                           "QPushButton{border:2px}"
        #                           "QPushButton{border-radius:10px}"
        #                           "QPushButton{padding:2px 4px}")
        # btn2.setProperty('name', 'btn2')

        # palette_red = QPalette()
        # palette_blue = QPalette()
        # palette_red.setColor(QPalette.Window, Qt.red)
        # palette_blue.setColor(QPalette.Window, Qt.blue)
        # self.Browser.setPalette(palette_blue)

        self.curveData = CurveData('Songxm')
        self.gridLayout = QGridLayout(self.groupBox) # 继承容器groupBox

    def machineTrigger(self, q):
        global setMachineMode, setTreeMode
        try:
            if q.text() == 'setMachine':
                setMachineMode=1
                self.Warning.clear()
                self.Warning.append('please select the data source')
                machineNames=['hl2a', 'localdas', 'east', 'exl50', 'hl2m']
                self.Files.clear()
                # show the machine in Files for select
                for m in machineNames:
                    self.Files.addItem(m)

            elif q.text() == 'ChnlConfig':  # modify the configuration
                self.hD = modifyConfig(self.curveData)
                self.hD.setWindowModality(Qt.ApplicationModal)
                self.hD.show()
                self.hD.signalCurve.connect(self.receiveCurveData)
                pass

            elif q.text() == 'scanTree':  # scan tree for channels
                myShot = self.shot.value()

                if self.mode == 0 or self.mode == 1:
                    pass
                elif self.mode == 2:
                    DPI.sct('exl50', myShot)
                elif self.mode == 3:
                    DPI.sct('east', myShot)

            elif q.text() == 'scanTreeAD':  # scan tree for channels
                myShot = self.shot.value()

                if self.mode == 0 or self.mode == 1:
                    pass
                elif self.mode == 2:
                    DPI.sctAD('exl50', myShot)
                elif self.mode == 3:
                    DPI.sctAD('east', myShot)


            elif q.text() == 'defaultChnl':  # modify the configuration
                self.defaultChnlSaveLoad()  # save

        except:
            self.Warning.append('machineTrigger' + ' or something wrong')
        else:
            self.Warning.append('machineTrigger' +' is OK')

    def processTrigger(self, q):
        global drawMode
        myShot = self.shot.value()
        if q.text() is 'setSystemName':

            if self.mode == 0 or self.mode==1:
                DPI.setSystemName(myShot)
            elif self.mode ==2:
                pass
            elif self.mode==3:
                pass

        elif q.text() == 'saveData':   # save data for later analysis
            path = 'C:\\DP\\data\\d' + str(myShot) + '.mat'
            # path = 'C:\\DP\\data\\'
            dataFile,_ =QFileDialog.getSaveFileName(self,'OpenFile',path,"matlab files (*.mat)")
            myCurves=self.curveData

            sio.savemat(dataFile, {'ChnlName': myCurves.ChnlName, 'X': myCurves.X, 'Y': myCurves.Y})
            # sio.savemat(dataFile, {'ChnlName': myCurves.ChnlName, 'X': myCurves.X, 'Y': myCurves.Y, 'myCurves': myCurves})
            pass
        elif q.text() == 'loadData':   # load data for analysis

            path='C:\\DP\\data\\'
            dataFile,_ =QFileDialog.getOpenFileName(self, 'OpenFile', path, "matlab files (*.mat)")
            f=sio.loadmat(dataFile)
            ChnlName=f['ChnlName']   #
            X=f['X']   #
            Y=f['Y']   #
            # myCurves=f['myCurves']

            self.Curves.clear()
            self.curveData = CurveData('Songxm')  # initializing the class

            for n in range(len(ChnlName)):
                channelName=ChnlName[n]
                self.Curves.addItem(channelName)
                x=X[n]
                y=Y[n]
                self.setCurveData(x, y, n, channelName, channelName)

        elif q.text() == 'saveConfig':  # save channel configuration for later use

            path='C:\\DP\\configuration\\'
            configFile,_ =QFileDialog.getSaveFileName(self,'OpenFile',path,"matlab files (*.mat)")
            myCurves=self.curveData
            myCurves.x=[]
            myCurves.y=[]
            sio.savemat(configFile, {'ChnlName': myCurves.ChnlName})
            pass

        elif q.text() == 'loadConfig':
            path='C:\\DP\\configuration\\'
            configFile,_ =QFileDialog.getOpenFileName(self,'OpenFile',path,"matlab files (*.mat)")
            f=sio.loadmat(configFile)
            Chnl=f['ChnlName']   # np.array

            self.hD = selectChnl(Chnl)
            self.hD.setWindowModality(Qt.ApplicationModal)
            self.hD.show()
            self.hD.signalChnl.connect(self.receiveChnl)

            pass
        elif q.text() == 'drawMode':

            number, ok = QInputDialog.getInt(self, "action", "0=mat,1=pyqtgrapg", drawMode, 0, 1, 1)
            if ok:
                drawMode = number

            self.draw.clicked.disconnect()

            if drawMode == 0:  # matlab mode
                self.draw.clicked.connect(self.drawClickedMat)
            elif drawMode == 1:  # pyqtgraph mode
                self.draw.clicked.connect(self.drawClicked)

            pass

    def helpTrigger(self,q):
        if q.text() == 'Basics':  # how to use
            self.Warning.append('---------------------------------------------------------------------------------' +
                                '\n[BASICS]\n' +
                                'Choosing a machine: click Machine and select setMachine from the drop down bar. Choose '
                                + 'desired machine listed in the Files module\n\n' +
                                'Searching for channel patterns: input regular expressions into search bar labeled '
                                + 'Search Chnl. Results will appear in the Browser module\n\n' +
                                'Adding channels to Curves: click Browser to change it to Browser+Add. You can now '
                                + 'select multiple channels which will be listed in the Curves module, and can be drawn, '
                                + 'updated, exported, etc\n\n' +
                                'Exporting/Importing channels: click File and select saveConfig/loadConfig\n\n' +
                                'For more information, click Help\n' +
                                '---------------------------------------------------------------------------------')
        elif q.text() == 'Buttons':
            self.Warning.append('---------------------------------------------------------------------------------' +
                                '\n[BUTTONS]\n' +
                                'shotOK: prepares work for data mining for shot\n' +
                                'update: reloads data based on current settings\n' +
                                'draw: displays multiple data side by side when in Browser+Add mode\n' +
                                'clearAll: clears entire interface\n' +
                                '---------------------------------------------------------------------------------')
        elif q.text() == 'Drop Down Menu':
            self.Warning.append('---------------------------------------------------------------------------------' +
                                '\n[DROP DOWN MENU]\n' +
                                'setSystemName: [INFO]\n' +
                                'saveConfig: saves current settings into external file\n' +
                                'saveData: [INFO]\n' +
                                'loadConfig: loads selected external file to update current settings\n' +
                                'setMachine: allows user to select machine, listed under Files\n' +
                                'ChnlConfig: allows user to modify the channel information\n' +
                                'defaultChnl: [INFO]\n' +
                                '---------------------------------------------------------------------------------')

    def receiveCurveData(self,dictCurves):  # dict

        sLabel = ['Num', 'Loc', 'Right', 'Color', 'Marker', 'LineStyle', 'FraNum', 'XOffset', 'YOffset',\
                  'Factor', 'Unit', 'Stairs', 'ChnlName', 'Min', 'Max']

        for i in range(len(sLabel)):
            cmd='self.curveData.' + sLabel[i] + '=dictCurves["' + sLabel[i] + '"]'
            exec(cmd)
        pass


    def defaultChnlSaveLoad(self, *args):
        path = 'C:\\DP\\configuration\\'

        if self.mode == 0:
            File='HL2ADefaultChnl.mat'
        elif self.mode == 1:
            File='localDefaultChnl.mat'
        if self.mode == 2:
            File='eastDefaultChnl.mat'
        elif self.mode == 3:
            File='exl50DefaultChnl.mat'

        configFile= path + File

        if len(args) == 0:

            Chnl=[]
            for i in range(self.Channels.count()):
                Chnl.append(self.Channels.item(i).text())

            sio.savemat(configFile, {'ChnlName': Chnl})

        elif len(args) == 1:
            if args[3]==1:

                f = sio.loadmat(configFile)
                Chnl = f['ChnlName']  # np.array

                self.Channels.clear()
                for i in range(len(Chnl)):
                    self.Channels.addItem(Chnl[i])
            else:
                pass
        else:
            pass


    def receiveChnl(self,Chnl):
        self.Curves.clear()
        for i in range(len(Chnl)):
            self.Curves.addItem(Chnl[i].strip())


    def initDP(self):
        self.hD = []
        self.hF = []
        self.mw = []
        self.gv = []
        self.l = []

        DPI.mode = self.mode  # initialize the DPI
        # initial help info
        self.Warning.append('---------------------------------------------------------------------------------' +
                            '\n[BASICS]\n' +
                            'Choosing a machine: click Machine and select setMachine from the drop down bar. Choose '
                            + 'desired machine listed in the Files module\n\n' +
                            'Searching for channel patterns: input regular expressions into search bar labeled '
                            + 'Search Chnl. Results will appear in the Browser module\n\n' +
                            'Adding channels to Curves: click Browser to change it to Browser+Add. You can now '
                            + 'select multiple channels which will be listed in the Curves module, and can be drawn, '
                            + 'updated, exported, etc\n\n' +
                            'Exporting/Importing channels: click File and select saveConfig/loadConfig\n\n' +
                            'For more information, click Help\n' +
                            '---------------------------------------------------------------------------------')
        # check if there is the folder machine to store the channel list
        treePath = os.path.join(os.getcwd(), 'machine')
        if not (os.path.exists(treePath)):
            os.mkdir(treePath)

        if self.mode==0:

            self.Warning.append('machine is HL2A')
            self.shot.setValue(DPI.getLatestShot())
        elif self.mode == 1:

            self.Warning.append('machine is Local DAS')
            self.shot.setValue(80020)
        elif self.mode == 2:
            if DPI.isMachineReady('exl50'):
                self.Warning.append('machine is exl50')
                currentShot = DPI.getLatestShot()
                self.shot.setValue(currentShot)
                treeChnlFile =os.path.join(os.getcwd(), 'machine\\exl50.mat')

                if not (os.path.exists(treeChnlFile)):
                    DPI.sct('exl50', currentShot)

            else:
                pass
                QMessageBox.information(self, 'machine', 'exl50 is not ready!', QMessageBox.Yes | QMessageBox.No)
        elif self.mode == 3:
            if DPI.isMachineReady('east'):

                self.Warning.append('machine is east')
                currentShot = DPI.getLatestShot()
                self.shot.setValue(currentShot)

                treeChnlFile = os.path.join(os.getcwd(), 'machine\\east.mat')

                if not (os.path.exists(treeChnlFile)):
                    DPI.sct('east', currentShot)

            else:
                pass
                QMessageBox.warning(self, 'machine', 'east is not ready!', QMessageBox.Yes | QMessageBox.No)

        # self.defaultChnlSaveLoad(1)  # Load
        # if drawMode == 0:  # matlab mode
        #     self.draw.clicked.connect(self.drawClickedMat)
        # elif drawMode == 1:  # pyqtgraph mode
        #     self.draw.clicked.connect(self.drawClicked)

    def view2Struct(self):
        global myStart, myEnd, myFrq
        try:
            myStart = float(self.xLeft.text())
            myEnd = float(self.xRight.text())
            myFrq = float(self.freqInterp.text())

            DPI.myStart = myStart
            DPI.myEnd = myEnd
            DPI.myFrq = myFrq
        except:
            self.Warning.append('xvalue' + ' or something wrong')
        else:
            self.Warning.append('xvalue' +' is OK')


    # pushbutton callback
    def clearOneClicked(self):
        # remove the current curves
        self.Curves.takeItem(self.Curves.currentRow())
        self.curveData.remove(self.Curves.currentRow())


    def clearAllClicked(self):
        # data to drawing the curves
        self.Curves.clear()
        self.curveData = CurveData('Songxm')  # initializing the class
        self.Warning.clear()
        self.Channels.clear()  # Clear browser



    def drawClicked(self):
        global trajectoryX, trajectoryY, trajectoryXData,  mouseDown, mouseMove, showInfMode
        global myWidth, myHeight, myDPI, oscilloscopeMode, isDrawConfigReady
        global myBox, hAxes, hVBs, hPIs, hGV, hLines, hLine1, vLine1, hLine2, vLine2, myText

        if isDrawConfigReady:
            self.initDrawConfig()

        hAxes=[]

        try:

            pg.setConfigOptions(antialias=True, background='w', foreground='k')
            self.mw = QtGui.QMainWindow()
            self.gv = pg.GraphicsView()

            self.mw.setCentralWidget(self.gv)
            self.l = QtGui.QGraphicsGridLayout()
            self.l.setHorizontalSpacing(0)
            self.l.setVerticalSpacing(0)
            self.gv.centralWidget.setLayout(self.l)

            self.mw.setWindowTitle('curves')
            self.mw.resize(1600, 800)

            # *********************************************
            # Dr SONG Xianming's comment
            # very important part of code
            # it connect the function to do the right thing for the event.
            # the event is from the signal defined in GraphicsView.py.
            self.gv.sigMousePressed.connect(on_button_presspg)
            self.gv.sigMouseReleased.connect(on_button_releasepg)
            self.gv.sigSceneMouseMoved.connect(motion_notifypg)
            self.gv.sigKeyPressed.connect(on_key_presspg)

            startTime=float(self.xLeft.text())  # in ms
            endTime=float(self.xRight.text())

            hAxes=[]
            hVBs=[]
            hPIs=[]

            # symbol 'o', 's', 't', 't1', 't2', 't3','d', '+', 'x', 'p', 'h', 'star'
            for i in range(len(self.Curves)):
                x=self.curveData.X[i]/1  # s->s
                x=np.reshape(x,(len(x)))
                y=self.curveData.Y[i]
                y=np.reshape(y,(len(x)))

                pi = pg.PlotItem()
                # pi = pg.PlotItem(name=self.curveData.ChnlName[i])
                # pi.addLegend(size=None,offset=(30,30))

                # pi.plot(x, y, pen='b', name=self.curveData.ChnlName[i])
                pi.plot(x, y, pen='b', name=self.curveData.ChnlName[i])
                # pi.plot(x, y, pen='b', name=self.curveData.ChnlName[i],symbolBrush=(255,0,0),symbolSize=8,symbol='o')
                # pi.plot(x, y+y/2, pen='r', name='cp',symbolBrush=(0,255,0),symbolSize=10,symbol='star')


                pi.showGrid(x=True, y=True)
                # pi.legend.addItem(pi,self.curveData.ChnlName[i])
                pi.setLabel('left',self.curveData.ChnlName[i])

                self.l.addItem(pi, i, 0)
                vb=pi.vb
                vb.setMouseMode(1)
                myScale = pi.getAxis('left')
                # myScale = sxm.SongAxis(orientation='left', showValues=True, maxTickLength=0)
                myScaleL=pi.getAxis('bottom')
                myScaleL.setStyle(showValues=False)

                myScaleT=pi.getAxis('top')
                myScaleT.setStyle(showValues=False)
                myScaleT.show()

                yLim=[float(self.curveData.Min[i]), float(self.curveData.Max[i])]
                newYLim, myTickY, myTickYLabel=sxm.MyYTick(yLim, tickNumber, 1, 0)
                vb.setYRange(newYLim[0], newYLim[1], padding=0.0, update=True)
                Ticks=[]
                for ii in range(len(myTickY)):

                    Ticks.append((myTickY[ii],myTickYLabel[ii]))

                myScale.setTicks([Ticks])
                hVBs.append(vb)
                hPIs.append(pi)
                hAxes.append(myScale)

            myScaleL.setStyle(showValues=True)

            for i in range(len(self.Curves)-1):
                hVBs[i].setXLink(hVBs[len(self.Curves)-1])

            for i in range(len(self.Curves) - 1):
                hVBs[i].setXRange(startTime, endTime, padding=0.0, update=True)



            myScaleX = pi.getAxis('bottom')
            myScaleX.show()
            myScaleX.linkToView(hVBs[len(self.Curves)-1])

            myBox = self.gv.scene().addRect(10000, 0, 300, 400, pen=pg.mkPen(color=pg.mkColor(255, 0, 0, 255), width=4))
            # for oscilloscopeMode
            hLine1 = self.gv.scene().addLine(10000, 200, 10000, 200, pen=pg.mkPen(color='r', width=2))
            vLine1 = self.gv.scene().addLine(10000, 0, 10000, 100, pen=pg.mkPen(color='r', width=2))
            hLine2 = self.gv.scene().addLine(10000, 100, 10000, 100, pen=pg.mkPen(color='b', width=2))
            vLine2 = self.gv.scene().addLine(10000, 0, 10000, 600, pen=pg.mkPen(color='b', width=2))

            myText = self.gv.scene().addText('hello world!')
            myText.setPos(10000,100)





        except:

            self.Warning.append('drawing' + ' or something wrong')
        else:
            self.Warning.append('drawing' +' is OK')
            self.mw.show()

    def drawClickedMat(self):

        global trajectoryX, trajectoryY, trajectoryXData,  mouseDown, mouseMove, showInfMode
        global myWidth, myHeight, myDPI, oscilloscopeMode
        global myBox, hAxes, hLines, hLine1, vLine1, hLine2, vLine2, myText
        hAxes = []

        try:
            currentShot=self.shot.value()
            # main_frame = QWidget()
            # fig=Figure(figsize=(myWidth, myHeight), dpi=myDPI)
            fig = plt.figure(figsize=(myWidth, myHeight), dpi=myDPI)
            fig.canvas.toolbar.hide()
            # fig.canvas.mpl_disconnect(fig.canvas.manager.key_press_handler_id)  # 取消默认快捷键的注册
            fig.canvas.mpl_disconnect('idle_event')
            fig.canvas.mpl_disconnect('draw_event')
            fig.canvas.mpl_disconnect('scroll_event')
            fig.canvas.mpl_disconnect('pick_event')
            fig.canvas.mpl_disconnect('figure_enter_event')
            fig.canvas.mpl_disconnect('figure_leave_event')
            fig.canvas.mpl_disconnect('axes_enter_event')
            fig.canvas.mpl_disconnect('axes_leave_event')
            fig.canvas.mpl_disconnect('resize_event')
            fig.canvas.mpl_disconnect('close_event')

            fig.canvas.mpl_connect("motion_notify_event", motion_notify)
            fig.canvas.mpl_connect('key_press_event', on_key_press)
            fig.canvas.mpl_connect('button_press_event', on_button_press)
            fig.canvas.mpl_connect('button_release_event', on_button_release)

            fig.suptitle(str(currentShot))

            for i in range(len(self.Curves)):
                if i > 0:
                    axes = plt.subplot(len(self.Curves), 1, i+1, sharex=hAxes[i-1])
                else:
                    axes = plt.subplot(len(self.Curves), 1, i+1)

                axes.spines['bottom'].set_linewidth(lineWidth)
                axes.spines['left'].set_linewidth(lineWidth)
                axes.spines['top'].set_linewidth(lineWidth)
                axes.spines['right'].set_linewidth(lineWidth)
                plt.tick_params(labelsize=fontSize)

                hAxes.append(axes)
                x=self.curveData.X[i]
                y=self.curveData.Y[i]

                # curve conditionning
                x=x+float(self.curveData.XOffset[i])
                y=y*float(self.curveData.Factor[i])+float(self.curveData.YOffset[i])

                if i < len(self.Curves)-1:

                    plt.setp(axes.get_xticklabels(), visible=False)

                line = plt.plot(x, y,label=self.Curves.item(i).text(), marker=self.curveData.Marker[i], color=self.curveData.Color[i], \
                                lw=4, ls=self.curveData.LineStyle[i])
                plt.legend()
                hLines.append(line)
                plt.grid(True)
                axes.tick_params(direction='in')

                yLim=[float(self.curveData.Min[i]), float(self.curveData.Max[i])]
                newYLim, myTickY, myTickYLabel=sxm.MyYTick(yLim, tickNumber, 1, 0)
                axes.set_ylim(newYLim)
                axes.set_yticks(myTickY)
                axes.set_yticklabels(myTickYLabel)

            plt.subplots_adjust(left=defaultPos[0], right=defaultPos[0]+defaultPos[2], bottom=defaultPos[1], top=defaultPos[1]+defaultPos[3], wspace=0.0, hspace=0.0)
            # plt.subplots_adjust(left=0.05, right=0.95, bottom=0.1, top=0.85, wspace=0.0, hspace=0.0)
            # all in myBox


            myBox = fig.add_axes([0, 0, 0, 0])
            myBox.patch.set_alpha(0.2)
            myBox.patch.set_color('r')
            plt.xticks(())
            plt.yticks(())
            # for oscilloscopeMode
            hLine1 = plt.plot([0, 0], [0, 0], ':r')
            vLine1 = plt.plot([0, 0], [0, 0], ':r')
            hLine2 = plt.plot([0, 0], [0, 0], ':m')
            vLine2 = plt.plot([0, 0], [0, 0], ':m')
            myText = plt.text(0, 0, '')

            plt.show()

        except:
            self.Warning.append('drawing' + ' or something wrong')
        else:
            self.Warning.append('drawing' +' is OK')
            self.hF=fig  # live is long

    def shotOKClicked(self):
        global setMachineMode
        myShot = self.shot.value()

        if self.mode == 2 or self.mode == 3:
            setMachineMode = 2  # east and exl50 total channels
            myInfDir = '.\\machine'
            myDirs=os.listdir(myInfDir)
            self.Files.clear()
            for F in myDirs:
                searchObj = re.search('.mat', F)
                if not (str(searchObj) == 'None'):
                    self.Files.addItem(F)
            self.Warning.append(str(myShot) + ' time stamp: ' + str(DPI.getDateTime('exl50',myShot)))


        elif self.mode == 0 or self.mode == 1 or self.mode == 4:
            setMachineMode = 0
            DPI.setSystemName(myShot)
            myDir = DPI.getDasDir(myShot)
            myShotName = '00000' + str(myShot)
            myShotName = myShotName[-5:]  # should be five character
            myInfDir = DPI.getDriver() + '\\' + myDir + '\\INF'
            myDirs=os.listdir(myInfDir)
            self.Files.clear()
            for F in myDirs:
                searchObj = re.search(myShotName, F)
                if not (str(searchObj) == 'None'):
                    self.Files.addItem(F)

    def initDrawConfig(self):
        global isDrawConfigReady
        index = self.layoutMode.currentIndex()
        if index==0:
            pass
        elif index==1:
            pass
        elif index==2:
            pass
        elif index==3:
            pass
        pass
        isDrawConfigReady = 1

    def xValueChanged(self):
        self.view2Struct()

    def fileClicked(self):
        global setMachineMode
        global machineName, treeNames

        try:
            if setMachineMode==1:  # select machine
                machineName=self.Files.currentItem().text()
                self.Channels.clear()  # Resets browser after file is selected
                setMachineMode = 0  # exit the setMachineMode
                if machineName == 'hl2a':
                    self.mode = 0
                    DPI.mode = self.mode
                    self.Warning.append('machine is HL2A')
                    currentShot = DPI.getLatestShot()
                    self.shot.setValue(currentShot)
                elif machineName == 'localdas':
                    self.mode = 1
                    DPI.mode = self.mode
                    self.shot.setValue(80021)
                    self.Warning.append('machine is LocalDas')
                if machineName == 'exl50':
                    self.mode = 2
                    DPI.mode = self.mode
                    self.Warning.append('machine is exl50')
                    currentShot = DPI.getLatestShot()
                    self.shot.setValue(currentShot)
                elif machineName == 'east':
                    self.mode = 3
                    DPI.mode = self.mode
                    self.Warning.append('machine is east')
                    currentShot = DPI.getLatestShot()
                    self.shot.setValue(currentShot)
                if machineName == 'hl2m':
                    self.mode = 4
                    DPI.mode = self.mode
                    self.Warning.append('machine is HL2M')
                    currentShot = DPI.getLatestShot()
                    self.shot.setValue(currentShot)

                self.Files.clear()

            elif setMachineMode==0:
                fileName=self.Files.currentItem().text()
                mySys=fileName[5:8]
                myShot=fileName[0:5]
                shotNumber=int(myShot)
                self.currentSys=mySys
                self.currentShot=shotNumber

                InfFileName = DPI.getInfFileName(shotNumber, mySys)
                infchs = InfChnl.InfChnls(InfFileName)
                cns = infchs.getChnls
                self.Channels.clear()
                for channel in cns:
                    self.Channels.addItem(channel)
            elif setMachineMode == 2:
                fileName=self.Files.currentItem().text()
                machineName=fileName[:-4]

                if machineName == 'exl50':
                    self.mode = 2
                    DPI.mode = self.mode
                    currentShot = DPI.getLatestShot()
                    self.shot.setValue(currentShot)
                    self.Warning.append('machine is exl50')
                    treeChnlFile = '.\\machine\\exl50.mat'

                elif machineName == 'east':
                    self.mode = 3
                    DPI.mode = self.mode
                    currentShot = DPI.getLatestShot()
                    self.shot.setValue(currentShot)
                    self.Warning.append('machine is east')
                    treeChnlFile = '.\\machine\\east.mat'

                a = sio.loadmat(treeChnlFile)
                chnl_sys = str(a['myChnlString'])

                # ??? why plus ';', more channel ignored, no return scan?
                # patternChnl = re.compile(';\w*' + channelName + '\w*;', re.I)

                patternChnl = re.compile(r'(?<=;)\w+(?=;)', re.I)  #(?= re) (?> re)
                chnlList = patternChnl.findall(chnl_sys)
                for channel in chnlList:
                    self.Channels.addItem(channel)

        except:
            self.Warning.append('fileClicked or something wrong')
        else:
            self.Warning.append('fileClicked is OK')

    def curveClicked(self,index):
        global setMachineMode
        global machineName, treeNames

        try:
            # self.Curves.currentItem().setBackground(Qt.red)
            # self.Curves.currentItem().setForeground(Qt.blue)
            # self.Curves.currentItem().setIcon(QIcon("C:\DataProc2A\MING32.BMP"))


            channelNameRaw = self.Curves.currentItem().text()
            channelName, ok = QInputDialog.getText(self, "modify", "chnl:", QLineEdit.Normal, channelNameRaw)
            if ok:
                # self.Curves.addItem(channelName)
                # self.Curves.insertItem(index,channelName)

                number, ok = QInputDialog.getInt(self, "action", "0=r,1=m,2=i,3=d", int(3), 0, 12, 2)
                if ok:
                    if number==0:
                        self.Curves.takeItem(index.row())
                    elif number==1:
                        self.Curves.currentItem().setText(channelName)

                    elif number==2:
                        self.Curves.insertItem(index.row(),channelName)

                    elif number==3:
                        self.defaultChnl=channelNameRaw
        except:
            self.Warning.append('fileClicked or something wrong')
        else:
            self.Warning.append('fileClicked is OK')

    def channelClicked(self):
        global setMachineMode
        global treeName
        try:
            self.Channels.setEnabled(False)
            channelNameRaw = self.Channels.currentItem().text()

            patternChnl = re.compile('\w+$', re.I)
            channelName = patternChnl.findall(channelNameRaw)[0]
            currentShot = self.shot.value()
            #  ms-> s
            startTime=self.xLeft.text()
            endTime=self.xRight.text()
            stepTime=self.freqInterp.text()
            timeContext= str(startTime) + ':' + str(endTime) + ':' + str(stepTime)

            if (showInfMode is 1):
                if (self.mode==0 or self.mode==1 or self.mode==4):
                    self.Warning.clear()
                    currentSys = DPI.getSystemName(channelName)
                    myInf=DPI.getInf(currentShot, channelName, currentSys)
                    self.Warning.append('ChnlName:' + myInf.ChnlName)
                    self.Warning.append('ChnlId:' + str(myInf.ChnlId))
                    self.Warning.append('Addr:' + str(myInf.Addr))
                    self.Warning.append('Freq:' + str(myInf.Freq))
                    self.Warning.append('Len:' + str(myInf.Len))
                    self.Warning.append('Post:' + str(myInf.Post))
                    self.Warning.append('MaxDat:' + str(myInf.MaxDat))
                    self.Warning.append('LowRang:' + str(myInf.LowRang))
                    self.Warning.append('HighRang:' + str(myInf.HighRang))
                    self.Warning.append('Factor:' + str(myInf.Factor))
                    self.Warning.append('Offset:' + str(myInf.Offset))
                    self.Warning.append('Unit:' + myInf.Unit)
                    self.Warning.append('Dly:' + str(myInf.Dly))
                    self.Warning.append('AttribDt:' + str(myInf.AttribDt))
                    self.Warning.append('DatWth:' + str(myInf.DatWth))
                    self.Warning.append('SparI1:' + str(myInf.SparI1))
                    self.Warning.append('SparI2:' + str(myInf.SparI2))
                    self.Warning.append('SparI3:' + str(myInf.SparI3))
                    self.Warning.append('SparF1:' + str(myInf.SparF1))
                    self.Warning.append('SparF2:' + str(myInf.SparF2))
                    self.Warning.append('SparC1:' + myInf.SparC1)
                    self.Warning.append('SparC2:' + myInf.SparC2)
                    self.Warning.append('SparC3:' + myInf.SparC3)
                    #           elif showInfMode is 0:
            else:
                if self.mode <2:
                    x, y, U = DPI.hl2adb(currentShot, channelName)
                elif self.mode==2:
                    x, y, U = DPI.exl50db(currentShot, channelName, timeContext)
                elif self.mode==3:
                    x, y, U = DPI.eastdb(currentShot, channelName, timeContext)
                elif self.mode==4:
                    x, y, U = DPI.hl2adb(currentShot, channelName)

                if self.browserMode is 1:
                    # initialize the   15

                    self.Curves.addItem(str(currentShot) + '\\' + channelName)
                    n=len(self.Curves)

                    self.setCurveData(x, y, n, str(currentShot) + '\\' + channelName, channelName)

                F = MyFigure(width=5, height=4, dpi=100)
                F.fig.suptitle(channelName)
                # F.axes = F.fig.add_subplot(111)
                F.axes.plot(x, y)
                self.gridLayout.addWidget(F, 0, 0)
                self.Channels.setEnabled(True)

        except:
            self.Warning.append(channelName + ' or something wrong')
            self.Channels.setEnabled(True)
        else:
            self.Warning.append(channelName +' is OK')

            self.Channels.setEnabled(True)

    def setCurveData(self, x, y, n, Label, channelName):
        self.curveData.Num.append(str(n))
        self.curveData.Loc.append(str(n))
        self.curveData.Right.append('1')  # min

        self.curveData.X.append(x)
        self.curveData.Y.append(y)
        self.curveData.Min.append(str(min(y)))  # min
        self.curveData.Max.append(str(max(y)))  # max
        self.curveData.Label.append(Label)  # for display channel
        self.curveData.Unit.append('au')
        self.curveData.ChnlName.append(channelName)  # for update channel
        self.curveData.Factor.append('1')
        self.curveData.XOffset.append('0')
        self.curveData.YOffset.append('0')
        self.curveData.Color.append('r')
        self.curveData.Marker.append('.')
        self.curveData.LineStyle.append('-')
        self.curveData.Stairs.append('1')  # ?
        self.curveData.FraNum.append('0')

    def browserClicked(self):
        if self.browserMode is 0:
            self.browserMode=1
            self.Browser.setText('Browser+Add')
            # self.Browser.setAutoFillBackground(True)
            self.Browser.setStyleSheet('background-color:green')
            self.Browser.setStyleSheet('Color:red')
            self.Browser.setStyleSheet("QPushButton:hover{color:blue}")

        else:
            self.browserMode = 0
            self.Browser.setText('Browser')
            self.Browser.setStyleSheet('background-color:black')
            self.Browser.setStyleSheet('Color:blue')
            self.Browser.setStyleSheet("QPushButton:hover{color:black}")


    def shotTogetherClicked(self):
        try:
            global progress, total

            myCurves = self.Curves
            currentShot=self.shot.value()
            #DPI.setSystemName(currentShot)

            self.hD = showProgress()
            self.hD.show()
            self.signalProgress.connect(self.hD.receiveProgress)

            #  ms-> s
            startTime=self.xLeft.text()
            endTime=self.xRight.text()
            stepTime=self.freqInterp.text()

            timeContext = str(startTime) + ':' + str(endTime) + ':' + str(stepTime)
            # timeContext=''
            total = len(myCurves)

            for i in range(len(myCurves)):
                currentChannelRaw = myCurves.item(i).text().strip()
                patternChnl = re.compile(r'\w+$', re.I)
                currentChannel = patternChnl.findall(currentChannelRaw)[0]

                # self.Warning.append('Progress: ' + str(i+1) + '/' + str(len(myCurves)))  # Progress info
                progress = i+1

                self.signalProgress.emit(progress, total)

                QApplication.processEvents()

                if self.mode < 2:
                    x, y, U = DPI.hl2adb(currentShot, currentChannel)
                elif self.mode == 2:
                    x, y, U = DPI.exl50db(currentShot, currentChannel,timeContext)
                elif self.mode == 3:
                    x, y, U = DPI.eastdb(currentShot, currentChannel,timeContext)

                self.Curves.addItem(str(currentShot) + '\\' + currentChannel)
                n = len(self.Curves)

                self.setCurveData(x, y, n, str(currentShot) + '\\' + currentChannel, currentChannel)

            self.drawClicked()
        except:
            self.Warning.append('update' + ' or something wrong')
        else:
            self.Warning.append('update' +' is OK')
            self.hD=[];
    def updateClicked(self):
        try:
            global progress,total

            myCurves = self.Curves
            currentShot=self.shot.value()
            #DPI.setSystemName(currentShot)

            self.hD = showProgress()
            self.hD.show()
            self.signalProgress.connect(self.hD.receiveProgress)

            #  ms-> s
            startTime = self.xLeft.text()
            endTime = self.xRight.text()
            stepTime = self.freqInterp.text()
            timeContext = str(startTime) + ':' + str(endTime) + ':' + str(stepTime)
            # timeContext=''
            self.curveData = CurveData('Songxm')  # initializing the class
            total = len(myCurves)

            for i in range(len(myCurves)):
                currentChannelRaw = myCurves.item(i).text().strip()
                patternChnl = re.compile(r'\w+$', re.I)
                currentChannel = patternChnl.findall(currentChannelRaw)[0]

                # self.Warning.append('Progress: ' + str(i+1) + '/' + str(len(myCurves)))  # Progress info
                progress = i+1

                self.signalProgress.emit(progress, total)

                QApplication.processEvents()

                if self.mode < 2:
                    x, y, U = DPI.hl2adb(currentShot, currentChannel)
                elif self.mode == 2:
                    x, y, U = DPI.exl50db(currentShot, currentChannel,timeContext)
                elif self.mode == 3:
                    x, y, U = DPI.eastdb(currentShot, currentChannel,timeContext)

                self.setCurveData(x, y, i, currentChannel, currentChannel)

            self.drawClicked()
        except:
            self.Warning.append('update' + ' or something wrong')
        else:
            self.Warning.append('update' +' is OK')
            self.hD=[]

    def chnlPatterntextChanged(self):
        try:
            mode=self.mode
            self.Channels.clear()
            myChnlPattern=self.chnlPattern.text()
            if mode>1:
                myChnlSysList = DPI.getChnlNode(myChnlPattern)
            else:
                myChnlSysList = DPI.getChnlPattern(myChnlPattern)

            for myChnlSys in myChnlSysList:
                self.Channels.addItem(myChnlSys)


        except:
            self.Warning.append('chnlPatterntextChanged' + ' or something wrong')
            self.Channels.setEnabled(True)
        else:
            self.Warning.append('chnlPatterntextChanged' + ' is OK')
            self.Channels.setEnabled(True)

    def WarningClicked(self):
        self.Warning.clear()

    def sortClicked(self):
        self.Channels.sortItems(order=Qt.AscendingOrder)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = mwindow()
    w.setWindowTitle("DP developed by Dr. SONG")

    w.Files.clicked.connect(w.fileClicked)
    w.Channels.clicked.connect(w.channelClicked)
    w.Curves.clicked.connect(w.curveClicked)

    if drawMode == 0:  # matlab mode
        w.draw.clicked.connect(w.drawClickedMat)
    elif drawMode == 1:  # pyqtgraph mode
        w.draw.clicked.connect(w.drawClicked)

    w.clearAll.clicked.connect(w.clearAllClicked)
    w.clearOne.clicked.connect(w.clearOneClicked)
    w.shotOK.clicked.connect(w.shotOKClicked)
    w.xLeft.textChanged.connect(w.xValueChanged)
    w.xRight.textChanged.connect(w.xValueChanged)
    w.freqInterp.textChanged.connect(w.xValueChanged)
    w.Browser.clicked.connect(w.browserClicked)
    # w.Warning.mouseDoubleClickEvent.connect(w.WarningClicked)
    w.update.clicked.connect(w.updateClicked)
    w.shotTogether.clicked.connect(w.shotTogetherClicked)
    w.chnlPattern.textChanged.connect(w.chnlPatterntextChanged)

    w.sort.clicked.connect(w.sortClicked)

    w.show()
    sys.exit(app.exec_())

