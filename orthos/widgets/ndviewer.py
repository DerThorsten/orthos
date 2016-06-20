

import numpy
import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
from pyqtgraph.dockarea import *
from pyqtgraph.parametertree import ParameterTree
from color_dock import *
import logging
from . import planeVector
from ndviewer_options import *



nameToPattern = {
    'SolidPattern': QtCore.Qt.SolidPattern,
    'LinearGradientPattern': QtCore.Qt.LinearGradientPattern,
    'Dense1Pattern': QtCore.Qt.Dense1Pattern,
    'Dense2Pattern': QtCore.Qt.Dense2Pattern,
    'Dense3Pattern': QtCore.Qt.Dense3Pattern,
    'Dense4Pattern': QtCore.Qt.Dense4Pattern,
    'Dense5Pattern': QtCore.Qt.Dense5Pattern,
    'Dense6Pattern': QtCore.Qt.Dense6Pattern,
    'Dense7Pattern': QtCore.Qt.Dense7Pattern,
    'NoBrush': QtCore.Qt.NoBrush,
    'HorPattern': QtCore.Qt.HorPattern,
    'VerPattern': QtCore.Qt.VerPattern,
    'CrossPattern': QtCore.Qt.CrossPattern,
    'BDiagPattern': QtCore.Qt.BDiagPattern,
    'FDiagPattern': QtCore.Qt.FDiagPattern,
    'DiagCrossPattern': QtCore.Qt.DiagCrossPattern
}

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
            brush.setStyle(nameToPattern[str(self.bgType)])
            brush.setColor(self.bgColor1)

        self.background.setBrush(brush)
    def setBackgroundColor(self):
        self.updateBackground() 

class ViewBoxWidget(QtGui.QWidget):
    def __init__(self,ndViewer, plane, parent=None):

        super(ViewBoxWidget,self).__init__(parent=parent)
        self.mainLayout = QtGui.QVBoxLayout()
        self.glayout = pg.GraphicsLayout()
        self.graphicsView = pg.GraphicsView()

        # the view box
        self.viewBox = TiledViewBox(ndViewer=ndViewer, plane=plane)

        # the scales
        self.xAxis = pg.AxisItem(orientation='bottom', linkView=self.viewBox)
        self.yAxis = pg.AxisItem(orientation='left', linkView=self.viewBox)
        #self.xScale.setLabel(text=aixsLetters[viewAxis[0]])
        #@self.yScale.setLabel(text=aixsLetters[viewAxis[1]])



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


class OpenGl3dWidget(QtGui.QWidget):
    def __init__(self, ndViewer):
        super(OpenGl3dWidget,self).__init__()
        self.ndViewer = ndViewer
        
        def _setupUI():
            self.mainLayout = QtGui.QHBoxLayout()
            self.setLayout(self.mainLayout)
        _setupUI()


class LayerStackCtrlWidget(QtGui.QWidget):
    def __init__(self, ndViewer):
        super(LayerStackCtrlWidget,self).__init__()
        self.ndViewer = ndViewer
        
        def _setupUI():
            self.mainLayout = QtGui.QHBoxLayout()
            self.setLayout(self.mainLayout)
        _setupUI()


class SettingsEditorDialog(QtGui.QDialog):

    def __init__(self,ndViewer, parent):
        super(SettingsEditorDialog, self).__init__(parent)
        
        self.resize(800,600)
        self.ndViewer = ndViewer
        self.layout = QtGui.QVBoxLayout()
        self.setLayout(self.layout) 

  
        self.paramTree = ParameterTree()
        self.paramTree.setParameters(self.ndViewer.options.p, showTop=False)
        self.layout.addWidget(self.paramTree)
    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.hide()
            event.accept()
        else:
            super(QtGui.QDialog, self).keyPressEvent(event)


# http://standards.freedesktop.org/icon-naming-spec/icon-naming-spec-latest.html
class NdViewerCtrlWidget(QtGui.QWidget,object):
    def __init__(self, ndViewer):
        super(NdViewerCtrlWidget,self).__init__()
        self.ndViewer = ndViewer
        self._setupUI()
        self.diag = SettingsEditorDialog(ndViewer=self.ndViewer,parent=self)
    def _setupUI(self):
        self.mainLayout = QtGui.QHBoxLayout()
        self.setLayout(self.mainLayout)



        exitAction = QtGui.QAction(QtGui.QIcon.fromTheme("accessories-text-editor"), 'Settings', self)
        #exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Settings editor')
        exitAction.triggered.connect(self.showSettingsEditor)

        
        toolbar = QtGui.QToolBar()
        toolbar.addAction(exitAction)
        toolbar.setIconSize(QtCore.QSize(20,20))
        self.mainLayout.addWidget(toolbar)

    def showSettingsEditor(self):
        self.diag.show()



class NdViewerWidget(QtGui.QWidget):
    def __init__(self, globalAxis):
        super(NdViewerWidget,self).__init__()

        # global options object
        self.options = NdViewerOptions(ndViewer=self)

        self.globalAxis = globalAxis
        self.nDim = len(self.globalAxis)
        self.shape = self.globalAxis.shape
        self.planes = planeVector([])

        # widgets
        self.area = MyDockArea()
        self.area.setParent(self)
        self.ctrlWidget = NdViewerCtrlWidget(self)
        self.layerStackCtrlWidget = LayerStackCtrlWidget(ndViewer=self)
        self.layerDock = ColorDock(name="Layers", color=(50,)*3)

        self._setupUI()


    def _setupUI(self):
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.ctrlWidget)
        self.mainLayout.addWidget(self.area)
        self.layerDock.addWidget(self.layerStackCtrlWidget)
        self.area.addDock(self.layerDock,'right')
    
    def paramValue(self, key):
        """ get the params value"""
        return self.options[key]

    def param(self, *args, **kwargs):
        """ get the param object"""
        return self.options.param(*args,**kwargs)

    def addOrthogonalPlaneViewer(self, plane, pos=None, otherDock=None):

        # add the plane
        plane.planeIndex = len(self.planes)
        self.planes.addPlane(plane)

        # color of the dock
        color = self._getDockColor(plane)
        # add the dock
        dock = ColorDock(name=plane.name, color=color)
        dock.setParent(self.area)
        # plance the dock
        self._placeDock(dock=dock, pos=pos, otherDock=otherDock)


        # the widget
        viewBoxWidget = ViewBoxWidget(ndViewer=self,plane=plane, parent=dock)
        dock.addWidget(viewBoxWidget)

        return dock





    def add3dViewer(self):
        if(self.ndim <= 2):
            raise RuntimeError("3d viewer needs at least 3 axis")
        assert  False



    def _getDockColor(self, plane):
        """ Helping function to get the color of the dock
        """
        color = (0,0,0)
        if plane.zAxis != -1:
            color = self.globalAxis[plane.zAxis].color[0:3]
        return color

    def _placeDock(self, dock, pos=None, otherDock=None):
        """ Helping function to place the docks
        """
        if otherDock is not None and pos is not None:
            self.area.addDock(dock,pos,otherDock)
        elif pos is not None:
            self.area.addDock(dock,pos,otherDock)
        else:
            self.area.addDock(dock)
        return dock


