import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg

app = QtGui.QApplication([])
mw = QtGui.QMainWindow()
mw.setWindowTitle('pyqtgraph example: ViewBox')
mw.show()
mw.resize(800, 600)

gv = pg.GraphicsView()
mw.setCentralWidget(gv)
l = QtGui.QGraphicsGridLayout()
l.setHorizontalSpacing(0)
l.setVerticalSpacing(0)


vb = pg.ViewBox(border='r')
p1 = pg.PlotDataItem(np.random.normal(size=100))
vb.addItem(p1)


## Just something to play with inside the ViewBox
class movableRect(QtGui.QGraphicsRectItem):
    def __init__(self, *args):
        QtGui.QGraphicsRectItem.__init__(self, *args)
        self.setAcceptHoverEvents(True)

    def hoverEnterEvent(self, ev):
        self.savedPen = self.pen()
        self.setPen(pg.mkPen(255, 255, 255))
        ev.ignore()

    def hoverLeaveEvent(self, ev):
        self.setPen(self.savedPen)
        ev.ignore()

    def mousePressEvent(self, ev):
        if ev.button() == QtCore.Qt.LeftButton:
            ev.accept()
            self.pressDelta = self.mapToParent(ev.pos()) - self.pos()
        else:
            ev.ignore()

    def mouseMoveEvent(self, ev):
        self.setPos(self.mapToParent(ev.pos()) - self.pressDelta)


rect = movableRect(QtCore.QRectF(0, 0, 0.5, 0.5))
rect.setPen(pg.mkPen(100, 200, 100))
vb.addItem(rect)

l.addItem(vb, 0, 1)
gv.centralWidget.setLayout(l)




#
# yScale = pg.AxisItem(orientation='left', linkView=vb)
# l.addItem(yScale, 0, 0)





p2 = pg.ViewBox(border='m')
p2.addItem(pg.PlotCurveItem([300,160,300,200,200,100], pen='m'))
l.addItem(p2, 1, 1)

p3 = pg.ViewBox(border='b')
p3.addItem(pg.PlotCurveItem([00,160,300,200,200,100], pen='c'))
l.addItem(p3, 2, 1)

p4 = pg.ViewBox(border='b')
p4.addItem(pg.PlotCurveItem([00,160,300,200,200,100], pen='m'))
l.addItem(p4, 3, 1)


#
# xScale4 = pg.AxisItem(orientation='bottom')
# l.addItem(xScale4, 0, 1)
# yScale4 = pg.AxisItem(orientation='left')
# l.addItem(yScale4, 1, 0)


# xScale.setLabel(text="<span style='color: #ff0000; font-weight: bold'>X</span> <i>Axis</i>", units="s")
# yScale.setLabel('Y Axis', units='V')


def rand(n):
    data = np.random.random(n)
    data[int(n * 0.1):int(n * 0.13)] += .5
    data[int(n * 0.18)] += 2
    data[int(n * 0.1):int(n * 0.13)] *= 5
    data[int(n * 0.18)] *= 20
    return data, np.arange(n, n + len(data)) / float(n)


def updateData():
    yd, xd = rand(10000)
    p1.setData(y=yd, x=xd)


yd, xd = rand(10000)
updateData()
vb.autoRange()

t = QtCore.QTimer()
t.timeout.connect(updateData)
t.start(50)



# axesOrientation1=['right','top']
#
# for ao in axesOrientation1:
#     myScale = pg.AxisItem(orientation=ao, showValues=False, maxTickLength=0)
#     l.addItem(myScale, 1, 1)
#
# axesOrientation=['left', 'bottom']
#
# for ao in axesOrientation:
#     myScale = pg.AxisItem(orientation=ao, showValues=True, maxTickLength=5)
#     l.addItem(myScale, 1, 1)


#
# for ao in axesOrientation:
#     myScale = pg.AxisItem(orientation=ao, showValues=False, maxTickLength=0)
#     l.addItem(myScale, 0, 0)

# for ao in axesOrientation:
#     myScale = pg.AxisItem(orientation=ao, showValues=False, maxTickLength=0)
#     l.addItem(myScale, 0, 1)
# for ao in axesOrientation:
#     myScale = pg.AxisItem(orientation=ao, showValues=False, maxTickLength=0)
#     l.addItem(myScale, 1, 0)


myScale = pg.AxisItem(orientation='bottom', showValues=True, maxTickLength=0)
l.addItem(myScale, 4, 1)
myScale.linkToView(vb)
myScale.linkToView(p2)
myScale.linkToView(p3)
myScale.linkToView(p4)

vb.setXLink(p4)
p2.setXLink(p4)
p3.setXLink(p4)


myScale1 = pg.AxisItem(orientation='left', showValues=True, maxTickLength=0)
l.addItem(myScale1, 0, 0)

myScale1.linkToView(vb)
myScale2 = pg.AxisItem(orientation='left', showValues=True, maxTickLength=0)
l.addItem(myScale2, 1, 0)
myScale2.linkToView(p2)
myScale3 = pg.AxisItem(orientation='left', showValues=True, maxTickLength=0)
l.addItem(myScale3, 2, 0)
myScale3.linkToView(p3)
myScale4 = pg.AxisItem(orientation='left', showValues=True, maxTickLength=0)
l.addItem(myScale4, 3, 0)
myScale4.linkToView(p4)


## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys

    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
