import numpy as np
from pyqtgraph.Qt import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import orthos
import h5py

from orthos.widgets import *
from orthos.layers import *
from orthos.data_source import *

pg.setConfigOptions(antialias=False,useOpenGL=True,useWeave=True)

app = QtGui.QApplication([])
mw = MainWindow()
mw.setWindowTitle('Orthos')
mw.show()
mw.resize(800, 600)






with vigra.Timer("create raw layer"):
    f = "/home/tbeier/datasets/hhess/data.h5"
    #f = "/media/tbeier/data/datasets/hhess/2x2x2nm_chunked/data.h5"
    rawSource = VigraChunkedArrayHdf5(file_name=f,dataset_name='data')
    rawLayer = GrayscaleLayer(name='raw',levels=[0,255],dataSource=rawSource,useLut=True)


with vigra.Timer("create paint layer"):
    # paint layer
    f = "/home/tbeier/Desktop/labels_out.h5"
    labelsSource = VigraChunkedArrayHdf5(file_name=f,dataset_name='data',shape=rawSource.shape,
                                         mode=vigra.HDF5Mode.ReadWrite, compression=vigra.Compression.ZLIB_FAST,
                                         chunk_shape=[64,64,64],dtype='uint8')
    paintLayer = PaintLayer(name="paint",dataSource=labelsSource)

    #paintLayer = SplinePaintLayer(name="paint",dataSource=labelsSource)



spatialShape = rawSource.shape




opt = LayerViewerOptions()
opt.spatialDimensions = 3
opt.hasTimeAxis = False

with vigra.Timer("create viewer"):
    viewerWidget = LayerViewerWidget(spatialShape=spatialShape, options=opt)
    mw.setCentralWidget(viewerWidget)

with vigra.Timer("add raw layer"):
    viewerWidget.addLayer(rawLayer)

with vigra.Timer("add paint layer"):
    viewerWidget.addLayer(paintLayer)



#data = numpy.random.ones(*spatialShape)*255
#data = data.astype('uint8')
#ds = NumpyArrayDataSource(data)
#for x in range(20):
#    pmapLayer = GrayscaleLayer(name='pmap%d'%x,levels='auto',dataSource=ds,useLut=True)
#    viewerWidget.addLayer(pmapLayer)

with vigra.Timer("range changed"):
    viewerWidget.rangeChanged()

def closeCallback():
    labelsSource.flushToDisk()
mw.closeCallback = closeCallback



## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
