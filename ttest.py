
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Qt import QtGui, QtCore
from pyqtgraph.Point import Point

#generate layout
mouseDown=0
currentX=0
currentY=0

app = QtGui.QApplication([])
win = pg.GraphicsWindow()
win.setWindowTitle('pyqtgraph example: crosshair')
label = pg.LabelItem(justify='right')
win.addItem(label)
p1 = win.addPlot(row=1, col=0)
p2 = win.addPlot(row=2, col=0)


region = pg.LinearRegionItem()
region1 = pg.LinearRegionItem(orientation=1)
region.setZValue(10)
# Add the LinearRegionItem to the ViewBox, but tell the ViewBox to exclude this
# item when doing auto-range calculations.
p2.addItem(region, ignoreBounds=True)
p2.addItem(region1, ignoreBounds=True)

#pg.dbg()
p1.setAutoVisible(y=True)


#create numpy arrays
#make the numbers large to show that the xrange shows data from 10000 to all the way 0
data1 = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
data2 = 15000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)

p1.plot(data1, pen="r")
p1.plot(data2, pen="g")

p2.plot(data1, pen="w")

def update():
    region.setZValue(10)
    minX, maxX = region.getRegion()
    p1.setXRange(minX, maxX, padding=0)

def update1():
    # region1.setZValue(10)
    minY, maxY = region1.getRegion()
    p1.setYRange(minY, maxY, padding=0)


region.sigRegionChanged.connect(update)
region1.sigRegionChanged.connect(update1)

def updateRegion(window, viewRange):
    rgn = viewRange[0]
    region.setRegion(rgn)

p1.sigRangeChanged.connect(updateRegion)

def updateRegion1(window, viewRange):
    rgn = viewRange[1]
    region1.setRegion(rgn)

p1.sigRangeChanged.connect(updateRegion1)

region.setRegion([1000, 2000])
region1.setRegion([18000, 20000])

#cross hair
vLine1 = pg.InfiniteLine(angle=90, movable=False)
hLine1 = pg.InfiniteLine(angle=0, movable=False)
vLine1.setPen(pg.mkPen(color='b'))
hLine1.setPen(pg.mkPen(color='b'))
vLine = pg.InfiniteLine(angle=90, movable=False)
hLine = pg.InfiniteLine(angle=0, movable=False)


p1.addItem(vLine1, ignoreBounds=True)
p1.addItem(hLine1, ignoreBounds=True)
p1.addItem(vLine, ignoreBounds=True)
p1.addItem(hLine, ignoreBounds=True)


vb = p1.vb
# vb.Border(Pen='r')

def mouseMoved(evt):
    global currentX, currentY, mouseDown
    pos = evt  # [0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        if index > 0 and index < len(data1):
            label.setText("<span style='font-size: 18pt'>x=%0.1f, </span>  <span style='color: red'> dx=%0.1f</span>,  \
             <span style='color: green'>dy=%0.1f</span>" % (mousePoint.x(), mousePoint.x()-currentX, mousePoint.y()-currentY))

        vLine1.setPos(mousePoint.x())
        hLine1.setPos(mousePoint.y())
def mousePress(evt):
    global currentX, currentY, mouseDown

    pos = evt  # [0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        # if index > 0 and index < len(data1):
        #     label.setText("<span style='font-size: 18pt'>x=%0.1f, </span>  <span style='color: red'> y1=%0.1f</span>,  \
        #      <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
        currentX=mousePoint.x()
        currentY=mousePoint.y()

        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())
        pass
def mouseRelease(evt):
    global currentX, currentY, mouseDown

    pos = evt  # [0]  ## using signal proxy turns original arguments into a tuple
    if p1.sceneBoundingRect().contains(pos):
        mousePoint = vb.mapSceneToView(pos)
        index = int(mousePoint.x())
        # if index > 0 and index < len(data1):
        #     label.setText("<span style='font-size: 18pt'>x=%0.1f, </span>  <span style='color: red'> y1=%0.1f</span>,  \
        #      <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
        currentX=mousePoint.x()
        currentY=mousePoint.y()

        vLine.setPos(mousePoint.x())
        hLine.setPos(mousePoint.y())
        pass


    #
    # proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=mouseMoved)
    # proxy1 = pg.SignalProxy(p1.scene().sigMousePressed, rateLimit=60, slot=MousePressed)


p1.scene().sigMouseMoved.connect(mouseMoved)
p1.scene().sigMousePress.connect(mousePress)
p1.scene().sigMouseRelease.connect(mouseRelease)

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()