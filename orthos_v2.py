import logging
import orthos2
from pyqtgraph.Qt import QtGui, QtCore

app = QtGui.QApplication([])

logging.basicConfig(level=logging.INFO)



globalAxis = orthos2.axisVectorFactory(shape=[10,11,12],axistags='xyz')
viewer = orthos2.NdViewerWidget(globalAxis=globalAxis)


xyzPlane = orthos2.plane(name="xy_z",xAxis=0, yAxis=1, zAxis=2)
xzyPlane = orthos2.plane(name="xz_y",xAxis=0, yAxis=2, zAxis=1)
yzxPlane = orthos2.plane(name="yz_x",xAxis=1, yAxis=2, zAxis=0)

dockXYZ = viewer.addOrthogonalPlaneViewer(xyzPlane,'left')
dockXZY = viewer.addOrthogonalPlaneViewer(xzyPlane,'right',dockXYZ)
dockYZX = viewer.addOrthogonalPlaneViewer(yzxPlane,'bottom',dockXYZ)
viewer.storeLayout()
viewer.show()
#s = viewer.area.maximizeViewerDock(dockXYZ)
#viewer.area.restoreState(s)
# viewer.area.moveDock(dockXZY,'above',dockYZX)
# viewer.area.moveDock(dockXYZ,'above',dockXZY)

QtGui.QApplication.instance().exec_()
