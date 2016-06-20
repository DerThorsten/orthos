from orthos_cpp import axis,axisVector,plane
from pyqtgraph.Qt import QtGui, QtCore
import widgets
import layer
from factories import *
from ndviewer import *
from tools import *
import operator


def check(a,b,op = operator.__eq__ ,msg=None):
    if not op(a,b):
        "op(a,b) == True failed:\n  a = %s \n  b = %s \n op = %s % " %(str(a),str(b),str(op) )
        raise RuntimeError()


def axisVectorFactory(shape, axistags):
    check(len(shape),len(axistags),msg='shape and axistags must have equal length')
    getColor = defaultAxisColor
    axisList = []
    for i,(s,t) in enumerate(zip(shape,axistags)):
        a = axis(shape=s,name=t,shortName=t,color=getColor(i))
        axisList.append(a)
    return axisVector(axisList)


