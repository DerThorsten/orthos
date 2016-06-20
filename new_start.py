import numpy
import orthos


"here where try a 4d"
shape = (150,)*4

class Axis(object):
    def __init__(self, name, shortName, shape, color=None, isChannelAxis=False, channelNames=None):
        pass

class DataSourceAxis(object):
    def __init__(self, dataAxis):
        self.dataAxis  = 


xAxis = Axis(name='X0-Axis',shortName='x0', shape=shape[0], color=orthos.colors.defaultAxisColor(0))
yAxis = Axis(name='X1-Axis',shortName='x1', shape=shape[1], color=orthos.colors.defaultAxisColor(1))
zAxis = Axis(name='X2-Axis',shortName='x2', shape=shape[2], color=orthos.colors.defaultAxisColor(2))
tAxis = Axis(name='X3-Axis',shortName='x3', shape=shape[3], color=orthos.colors.defaultAxisColor(3))

# channel axis do not need a color
rgbAxis = Axis(name='RGB',shortName='RGB',shape=shape[3])

globalAxis = [xAxis, yAxis, zAxis, tAxis]


# negative number indicate channel axis
rawSource = DataSourceAxis(dataAxis=[0,1,2,3,4])
rgbSource = DataSourceAxis(dataAxis=dataAxis, axisOrdering=[0,1,2,3,4],channels=None)

# negative number indicate channel axis
rgbChannel = Channel(name='RGB',channelNames=['r','g','b'], shape=3)
rgbSource = DataSourceAxis(dataAxis=dataAxis, axisOrdering=[0,1,2,3,4,-1],channels=[rgbChannel])
