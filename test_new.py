import orthos
from pyqtgraph.Qt import QtGui, QtCore

app = QtGui.QApplication([])

############################################
# Declare Global Axis
############################################
getColor = orthos.colors.defaultAxisColor
xAxis = orthos.axis(shape=10, name="X-Axis", shortName='x', color=getColor(0))
yAxis = orthos.axis(shape=11, name="Y-Axis", shortName='y', color=getColor(1))
zAxis = orthos.axis(shape=12, name="Z-Axis", shortName='z', color=getColor(2))
tAxis = orthos.axis(shape=13, name="T-Axis", shortName='t', color=getColor(3))
globalAxis = orthos.axisVector([xAxis,yAxis,zAxis,tAxis])


############################################
# construct the viewer
############################################
viewer = orthos.widgets.NdViewerWidget(globalAxis = globalAxis)

############################################
# add plane to the viewer
#############################################
xyzPlane = orthos.plane(name="xy_z",xAxis=0, yAxis=1, zAxis=2)
xzyPlane = orthos.plane(name="xz_y",xAxis=0, yAxis=2, zAxis=1)
yzxPlane = orthos.plane(name="yz_x",xAxis=1, yAxis=2, zAxis=0)

dockXYZ = viewer.addOrthogonalPlaneViewer(xyzPlane,'left')
dockXZY = viewer.addOrthogonalPlaneViewer(xzyPlane,'right',dockXYZ)
dockYZX = viewer.addOrthogonalPlaneViewer(yzxPlane,'bottom',dockXYZ)

############################################
# launch the viewer
############################################
viewer.show()

############################################
# execute the app
############################################
QtGui.QApplication.instance().exec_()
