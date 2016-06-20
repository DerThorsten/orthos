import pyqtgraph as pg
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui


class OpenGl3dWidget(QtGui.QWidget):
    def __init__(self, ndViewer):
        super(OpenGl3dWidget,self).__init__()
        self.ndViewer = ndViewer
        
        def _setupUI():
            self.mainLayout = QtGui.QHBoxLayout()
            self.setLayout(self.mainLayout)
        _setupUI()
