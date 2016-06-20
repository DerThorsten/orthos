import pyqtgraph.opengl as gl
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from tiled_view_box import TiledViewBox

class TiledViewBoxWidget(QtGui.QWidget):
    def __init__(self,ndViewer, plane, parent=None):

        super(TiledViewBoxWidget,self).__init__(parent=parent)
        self.mainLayout = QtGui.QVBoxLayout()
        self.glayout = pg.GraphicsLayout()
        self.graphicsView = pg.GraphicsView()

        # the view box
        self.viewBox = TiledViewBox(ndViewer=ndViewer, plane=plane)

        # the scales
        self.xAxis = pg.AxisItem(orientation='bottom', linkView=self.viewBox)
        self.yAxis = pg.AxisItem(orientation='left', linkView=self.viewBox)

        # parameter interaction
        p = ndViewer.param('ViewBox Options','Show Axis')
        def showAxisChanged(param, changes):
            if changes == True:
                self.glayout.addItem(self.xAxis,2,1)
                self.glayout.addItem(self.yAxis,1,0)
            else:
                self.glayout.removeItem(self.xAxis)
                self.glayout.removeItem(self.yAxis)
        p.sigValueChanged.connect(showAxisChanged)


        def setupUI():
            # set the main layout
            self.setLayout(self.mainLayout)

            # make the graphics-view  the central widget
            self.mainLayout.addWidget(self.graphicsView)

            # add layout to graphics-view
            self.graphicsView.setCentralItem(self.glayout)

            # add items to layout
            self.glayout.addItem(self.viewBox,1,1)

        #  layouting etc
        setupUI()
