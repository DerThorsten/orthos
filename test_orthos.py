import vigra
import orthos
from nose.tools import eq_



class NumpyArraySource(object):
    def __init__(self, array, globalAxis, ownAxis):
        self.array = array
        self.globalAxis = globalAxis
        self.ownAxis = ownAxis

    def getSlice(self, globalSlicing, sliceAxis):
        pass



def test_axis():
    
    # declare global axis
    #  xyzt
    xAxis = orthos.axis(shape=10, name="X-Axis", shortName='x', color=orthos.colors.defaultAxisColor(0))
    yAxis = orthos.axis(shape=11, name="Y-Axis", shortName='y', color=(100,100,100), isChannelAxis=False, channelNames=orthos.StringVector())
    zAxis = orthos.axis(shape=12, name="Z-Axis", shortName='z')
    tAxis = orthos.axis(shape=13, name="T-Axis", shortName='t')
    rgbAxis = orthos.axis(shape=3, name="RGB", shortName='c',isChannelAxis=True)

    xAxis.isChannelAxis() == False
    rgbAxis.isChannelAxis() == True

    # the global axis ordering of the viewer
    globalAxis = orthos.axisVector([xAxis, yAxis, zAxis, tAxis])
    assert globalAxis.shape == [10, 11, 12, 13]
    assert globalAxis.hasSingletonAxis() == False
    assert globalAxis.hasChannelAxis() == False


    # now a source is in txyz
    sourceAAxis = orthos.axisVector([tAxis, xAxis, yAxis, zAxis])
    assert sourceAAxis.shape == [13, 10, 11, 12]
    assert sourceAAxis.hasSingletonAxis() == False
    assert sourceAAxis.hasChannelAxis() == False

    # now a source is in tzxyc
    sourceBAxis = orthos.axisVector([tAxis, zAxis, yAxis, xAxis, rgbAxis])
    assert sourceBAxis.shape == [13, 12, 11, 10, 3]
    eq_(sourceBAxis.nChannelAxis(),1)t
    assert sourceBAxis.hasSingletonAxis() == False
    assert sourceBAxis.hasChannelAxis() == True


    # find the mapping
    mapping = globalAxis.findAxis(sourceAAxis)
    print mapping

    # find the mapping
    mapping = globalAxis.findAxis(sourceBAxis)
    print mapping





    assert globalAxis.hasChannelAxis() == False
    eq_(globalAxis.nChannelAxis(),0)
    eq_(len(globalAxis),4)

    print xAxis
    print yAxis
    print zAxis
    print globalAxis

    xyzPlane = orthos.plane(name="xy_z",xAxis=0, yAxis=1, zAxis=2)
    xzyPlane = orthos.plane(name="xz_y",xAxis=0, yAxis=2, zAxis=1)
    yzxPlane = orthos.plane(name="yz_x",xAxis=1, yAxis=2, zAxis=0)

    planeVector = orthos.planeVector([xyzPlane, xzyPlane, yzxPlane9])

def run_tests():

    test_axis()

run_tests()
