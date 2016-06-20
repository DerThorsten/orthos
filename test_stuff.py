import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import orthos
import h5py

from orthos.widgets import *
from orthos.layers import *
from orthos.data_source import *

pg.setConfigOptions(antialias=False,useOpenGL=True)

app = QtGui.QApplication([])
mw = MainWindow()
mw.setWindowTitle('Orthos')
mw.show()
mw.resize(800, 600)




a = "/home/tbeier/Desktop/raw_gt.h5"
b= "/home/tbeier/Desktop/sampleA_mcseg.h5"


raw = numpy.array(vigra.impex.readHDF5(a,'data').view(numpy.ndarray).squeeze())
seg = numpy.array(vigra.impex.readHDF5(b,'data').view(numpy.ndarray).squeeze())




print "start"
opt = LayerViewerOptions()
opt.spatialDimensions = 3
opt.hasTimeAxis = False

viewerWidget = LayerViewerWidget(spatialShape=raw.shape, options=opt)
mw.setCentralWidget(viewerWidget)



with vigra.Timer("create raw layer"):
    f = "/home/tbeier/Desktop/input/raw.h5"
    #f = "/media/tbeier/data/datasets/hhess/2x2x2nm_chunked/data.h5"
    rawSource = NumpyArrayDataSource(raw.astype('uint8'))
    rawLayer = GrayscaleLayer(name='raw',levels='auto',dataSource=rawSource,useLut=True)
    viewerWidget.addLayer(rawLayer)


    svSource = NumpyArrayDataSource(seg)
    superVoxelLayer = SupervoxelLayer(name='sv',dataSource=svSource)
    objectLayer = ObjectLayer(name='obj',dataSource=svSource)

    viewerWidget.addLayer(superVoxelLayer)
    viewerWidget.addLayer(objectLayer)










with vigra.Timer("range changed"):
    viewerWidget.rangeChanged()




## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
