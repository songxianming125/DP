# -*- coding: utf-8 -*-
"""
Demonstrates use of PlotWidget class. This is little more than a
GraphicsView with a PlotItem placed in its center.
"""


from pyqtgraph.Qt import QtGui, QtCore
import numpy as np
import pyqtgraph as pg

#QtGui.QApplication.setGraphicsSystem('raster')
app = QtGui.QApplication([])
#mw = QtGui.QMainWindow()
#mw.resize(800,800)


def boxOn(p):
    # p.showAxis('top', False)
    # p.showAxis('bottom', False)
    # p.showAxis('right', False)
    # p.showAxis('left', False)
    p.showAxis('top', True)
    p.showAxis('bottom', True)
    p.showAxis('right', True)
    p.showAxis('left', True)
    # p.axes['bottom']['item'].setStyle(showValues=False)
    # p.axes['top']['item'].setStyle(showValues=False)
    # p.axes['right']['item'].setStyle(showValues=False)
    # p.axes['left']['item'].setStyle(showValues=False)
    pass

win = pg.GraphicsWindow(title="Basic plotting examples",border=True)
win.resize(1000,600)
win.setWindowTitle('pyqtgraph example: Plotting')

# Enable antialiasing for prettier plots
pg.setConfigOptions(antialias=True)

p1 = win.addPlot(y=np.random.normal(size=100),border=pg.mkPen(color='r'))

boxOn(p1)
p2 = win.addPlot()
p2.plot(np.random.normal(size=100), pen=(255,0,0), name="Red curve")
p2.plot(np.random.normal(size=110)+5, pen=(0,255,0), name="Green curve")
p2.plot(np.random.normal(size=120)+10, pen=(0,0,255), name="Blue curve")

boxOn(p2)
p3 = win.addPlot(border=pg.mkPen(color='r'))
p3.plot(np.random.normal(size=100), pen=(200,200,200), symbolBrush=(255,0,0), symbolPen='w')
boxOn(p3)

win.nextRow()

p4 = win.addPlot()
x = np.cos(np.linspace(0, 2*np.pi, 1000))
y = np.sin(np.linspace(0, 4*np.pi, 1000))
p4.plot(x, y)
p4.showGrid(x=True, y=True)

p5 = win.addPlot()
x = np.random.normal(size=1000) * 1e-5
y = x*1000 + 0.005 * np.random.normal(size=1000)
y -= y.min()-1.0
mask = x > 1e-15
x = x[mask]
y = y[mask]
p5.plot(x, y, pen=None, symbol='t', symbolPen=None, symbolSize=10, symbolBrush=(100, 100, 255, 50))
# p5.setLabel('left', "Y Axis", units='A')
# p5.setLabel('bottom', "Y Axis", units='s')
p5.setLogMode(x=True, y=False)

p6 = win.addPlot()
curve = p6.plot(pen='y')
data = np.random.normal(size=(10,1000))
ptr = 0
def update():
    global curve, data, ptr, p6
    curve.setData(data[ptr%10])
    if ptr == 0:
        p6.enableAutoRange('xy', False)  ## stop auto-scaling after the first data set is plotted
    ptr += 1
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)


win.nextRow()

p7 = win.addPlot()
y = np.sin(np.linspace(0, 10, 1000)) + np.random.normal(size=1000, scale=0.1)
p7.plot(y, fillLevel=-0.3, brush=(50,50,200,100))



x2 = np.linspace(-100, 100, 1000)
data2 = np.sin(x2) / x2
p8 = win.addPlot()
p8.plot(data2, pen=(255,255,255,200))
lr = pg.LinearRegionItem([400,700])
lr.setZValue(0)
p8.addItem(lr)

p9 = win.addPlot()
p9.plot(data2)
boxOn(p4)
boxOn(p5)
boxOn(p6)
boxOn(p7)
boxOn(p8)
boxOn(p9)

def updatePlot():
    p9.setXRange(*lr.getRegion(), padding=0)
def updateRegion():
    lr.setRegion(p9.getViewBox().viewRange()[0])




lr.sigRegionChanged.connect(updatePlot)
p9.sigXRangeChanged.connect(updateRegion)
updatePlot()

## Start Qt event loop unless running in interactive mode or using pyside.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
