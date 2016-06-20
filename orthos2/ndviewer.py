import logging
import numpy
import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from orthos_cpp import planeVector
from ndviewer_options import *
from plane_viewer import TiledViewBoxWidget
from widgets import ColorDockArea, ColorDock
from layer import LayerStackCtrlWidget
from tools import *

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
class NdViewerCtrlWidget(QtGui.QToolBar,object):
    def __init__(self, ndViewer):
        # fuck that shit, python is stupid
        # the self in the with statement cannot be used
        # without the next ridiculous line of code
        #self = self
        super(NdViewerCtrlWidget,self).__init__()
        with ScopeLogger("Construct NdViewerCtrlWidget"):
            
            self.ndViewer = ndViewer
            self._setupUI()
            self.diag = SettingsEditorDialog(ndViewer=self.ndViewer,parent=self)
    def _setupUI(self):
        #self.mainLayout = QtGui.QHBoxLayout()
        #self.setLayout(self.mainLayout)



        exitAction = QtGui.QAction(QtGui.QIcon.fromTheme("accessories-text-editor"), 'Settings', self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip('Settings editor')
        exitAction.triggered.connect(self.showSettingsEditor)

        
        #toolbar = QtGui.QToolBar()
        self.addAction(exitAction)
        self.setIconSize(QtCore.QSize(15,15))
        #self.mainLayout.addWidget(toolbar,2)

    def showSettingsEditor(self):
        self.diag.show()




class NdViewerWidget(QtGui.QWidget):
    def __init__(self, globalAxis):
        super(NdViewerWidget,self).__init__()
        with ScopeLogger("Construct NdViewerWidget"):
            

            # global options object
            self.options = NdViewerOptions(ndViewer=self)

            self.globalAxis = globalAxis
            self.nDim = len(self.globalAxis)
            self.shape = self.globalAxis.shape
            self.planes = planeVector([])

            # widgets
            self.area = ColorDockArea()
            self.area.setParent(self)
            self.ctrlWidget = NdViewerCtrlWidget(self)
            self.ctrlWidget.setFixedHeight(20)
            self.layerStackCtrlWidget = LayerStackCtrlWidget(ndViewer=self)
            self.layerDock = ColorDock(name="Layers", color=(50,)*3)

            self._setupUI()


    def _setupUI(self):
        self.mainLayout = QtGui.QVBoxLayout()
        self.setLayout(self.mainLayout)
        self.mainLayout.addWidget(self.ctrlWidget)
        self.mainLayout.addWidget(self.area,4)
        self.layerDock.addWidget(self.layerStackCtrlWidget)
        self.area.addDockToViewer(self.layerDock,'right')
    
    def paramValue(self, key):
        """ get the params value"""
        return self.options[key]

    def param(self, *args, **kwargs):
        """ get the param object"""
        return self.options.param(*args,**kwargs)

    def addOrthogonalPlaneViewer(self, plane, pos=None, otherDock=None):

        with ScopeLogger(" addOrthogonalPlaneViewer"):
            # add the plane
            plane.planeIndex = len(self.planes)
            self.planes.addPlane(plane)

            # color of the dock
            color = self._getDockColor(plane)
            # add the dock
            dock = ColorDock(name=plane.name, color=color)
            dock.isViewerDock = True
            dock.setParent(self.area)
            # plance the dock
            self._placeDock(dock=dock, pos=pos, otherDock=otherDock)


            # the widget
            viewBoxWidget = TiledViewBoxWidget(ndViewer=self,plane=plane, parent=dock)
            dock.addWidget(viewBoxWidget)

        return dock


    def storeLayout(self):
        self.area.storedLayout = self.area.saveState()


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
            self.area.addDockToViewer(dock,pos,otherDock)
        elif pos is not None:
            self.area.addDockToViewer(dock,pos,otherDock)
        else:
            self.area.addDockToViewer(dock)
        return dock


