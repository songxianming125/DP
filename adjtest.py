# encoding=utf-8
import pyqtgraph as pg
from PyQt5 import QtCore, QtGui
import numpy as np

# 简化建立app的过程
pg.mkQApp()

# 建立一个画布
pw = pg.PlotWidget()
# pw.show()
# 设置标题
pw.setWindowTitle('pyqtgraph example: MultiplePlotAxes')
# 定义一个画图小样？
p1 = pw.plotItem
# 给轴添加名称
p1.setLabels(left='axis 1')

# 定义一个视窗
p2 = pg.ViewBox()
# 显示某个轴 hide是隐藏
p1.showAxis('right')

# 添加小样到p1
p1.scene().addItem(p2)

# linkToView
# 绑定x y 轴
p1.getAxis('right').linkToView(p2)
p2.setXLink(p1)
p1.getAxis('right').setLabel('axis2', color='#0000ff')
p1.hideAxis('right')


p3 = pg.ViewBox()
ax3 = pg.AxisItem('right')
ax3.setGrid(True)

p1.layout.addItem(ax3,2,3)
p1.scene().addItem(p3)
# 隐藏轴
ax3.hide()

p4 = pg.ViewBox()
ax4 = pg.AxisItem('right')
ax4.setGrid(True)
ax4.hide()

p1.layout.addItem(ax4, 2, 1)
p1.scene().addItem(p4)

ax3.linkToView(p3)
p3.setXLink(p1)
ax3.setZValue(-10000)
ax3.setLabel('axis 3', color='#ff0000')

ax4.linkToView(p4)
p4.setXLink(p1)
ax4.setZValue(-10000)
ax4.setLabel('axis 4', color='#ff5555')


def updateViews():
    global p1, p2, p3, p4
    p2.setGeometry(p1.vb.sceneBoundingRect())
    p3.setGeometry(p1.vb.sceneBoundingRect())
    p4.setGeometry(p1.vb.sceneBoundingRect())

    p2.linkedViewChanged(p1.vb, p2.XAxis)
    p3.linkedViewChanged(p1.vb, p3.XAxis)
    p4.linkedViewChanged(p1.vb, p4.XAxis)

updateViews()
# p1.vb.sigResized.connect(updateViews)


p1.plot([1,2,4,8,16,32])
p1.showGrid(x=2, y=2)
p2.addItem(pg.PlotCurveItem([10,20,40,80,40,20], pen='b'))
p3.addItem(pg.PlotCurveItem([3200,1600,800,400,200,100], pen='r'))
p4.addItem(pg.PlotCurveItem([00,160,300,200,200,100], pen='m'))
pw.show()

if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()