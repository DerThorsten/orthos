import numpy
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui
from ..tools import getQtPattern

class TiledViewBox(pg.ViewBox):
    def __init__(self, ndViewer, plane, parent=None):

        pv = ndViewer.paramValue
        self.bgType  = pv(('ViewBox Options','ViewBox Background','bg-type'))
        self.bgColor1 = pv(('ViewBox Options','ViewBox Background','bg-color 1'))
        self.bgColor2 = pv(('ViewBox Options','ViewBox Background','bg-color 2'))
        super(TiledViewBox,self).__init__(invertY=True,lockAspect=True)
        self.ndViewer = ndViewer
        self.plane = plane
        # connect background parameters
        for c in ndViewer.param('ViewBox Options','ViewBox Background').children():
            c.sigValueChanged.connect(self.backgroundChanged)

        # rect changed
        self.sigXRangeChanged.connect(self.rectChanged)
        self.sigYRangeChanged.connect(self.rectChanged)

        self.updateBackground()
    def rectChanged(self):
        self.updateBackground()

    def backgroundChanged(self, param, changes):
        pv = self.ndViewer.paramValue
        self.bgType  = pv(('ViewBox Options','ViewBox Background','bg-type'))
        self.bgColor1 = pv(('ViewBox Options','ViewBox Background','bg-color 1'))
        self.bgColor2 = pv(('ViewBox Options','ViewBox Background','bg-color 2'))

        self.updateBackground()

    def updateBackground(self):
        self.background.show()
        self.background.setVisible(True)
        if self.bgType == 'LinearGradientPattern':
            g =  QtGui.QLinearGradient(
                                       QtCore.QRectF(self.rect()).topLeft(),
                                       QtCore.QRectF(self.rect()).bottomLeft()
            )
            g.setColorAt(0, self.bgColor1);
            g.setColorAt(1, self.bgColor2);
            brush = QtGui.QBrush(g)
        else:
            brush = QtGui.QBrush()
            brush.setStyle(getQtPattern(self.bgType))
            brush.setColor(self.bgColor1)

        self.background.setBrush(brush)
    def setBackgroundColor(self):
        self.updateBackground() 
