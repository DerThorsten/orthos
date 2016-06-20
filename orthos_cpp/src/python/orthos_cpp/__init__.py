# In theory, the extension already imports vigra for us.
# But for some reason that doesn't seem to work on all systems.
# The quick workaround is to just import it here.
import vigra
import numpy
from _orthos_cpp import *


def injector(classToExtend):

    class injectorCls(object):
        class __metaclass__(classToExtend.__class__):
            def __init__(self, name, bases, dict):
                for b in bases:
                    if type(b) not in (self, type):
                        for k,v in dict.items():
                            setattr(b,k,v)
                return type.__init__(self, name, bases, dict)
    return injectorCls




def axis(shape, name=None, shortName=None, color=(-1,-1,-1,-1), 
         isChannelAxis=False , channelNames=StringVector()):
    
    c = [int(c) for c in color]
    return _orthos_cpp._axis(
        shape = int(shape),
        name = name,
        shortName = shortName,
        color = c,
        isChannelAxis=bool(isChannelAxis),
        channelNames=channelNames
    )


def axisVector(axis=[]):
    axisVector = AxisVector()
    for a in axis:
        axisVector.addAxis(a)
    return axisVector


def plane(name, xAxis, yAxis, zAxis=-1):
    return Plane(name=name, xAxis=int(xAxis),
                 yAxis=int(yAxis), zAxis=int(zAxis))
    

def planeVector(planes=[]):
    vector = PlaneVector()
    for p in planes:
        vector.addPlane(p)
    return vector


class MoreAxis(injector(Axis),Axis):

    def __str__(self):
        out = "[name=%s, shortName=%s, shape=%d"%(self.name, self.shortName, self.shape)
        if self.hasColor():
            out += ", color=%s"%str(self.color)
        if self.isChannelAxis():
            out =", channelAxis"
        out +="]"
        return out

class MoreAxisVector(injector(AxisVector),AxisVector):

    def __str__(self):
        out = ""
        for ai in range(len(self)):
            axis = self[ai]
            out += "Axis %d %s"%(ai,str(axis))
            if ai != len(self)-1:
                out +="\n"
        return out

class MoreTileInfo(injector(TileInfo), TileInfo):


    def slicing3d(self):
        begin = self.roi3d.begin
        end   = self.roi3d.end
        return tuple([slice(b,e) for b,e in zip(begin,end)])
    


    def slicing2d(self):
        begin = self.roi2d.begin
        end   = self.roi2d.end
        return tuple([slice(b,e) for b,e in zip(begin,end)])








class ValToRgba(object):


    dtypeDict = {
        numpy.uint8          : 'uint8',
        numpy.uint16         : 'uint16',
        numpy.uint32         : 'uint32',
        numpy.uint64         : 'uint64',
        numpy.int8           : 'int8',
        numpy.int16          : 'int16',
        numpy.int32          : 'int32',
        numpy.int64          : 'int64',
        numpy.float32        : 'float32',
        numpy.float64        : 'float64',
        numpy.dtype('uint8') : 'uint8',
        numpy.dtype('uint32') : 'uint32',
        numpy.dtype('uint64') : 'uint64'
    }

    @classmethod
    def normalizeAndColormap(cls, dtype):
        dtypeStr = ValToRgba.dtypeDict[dtype]
        cls = _orthos_cpp.__dict__['NormalizedExplicitLut_%s'%dtypeStr]
        return cls

    @classmethod
    def uintColormap(cls, dtype):
        dtypeStr = ValToRgba.dtypeDict[dtype]
        cls = _orthos_cpp.__dict__['UIntExplicitLut_%s'%dtypeStr]
        return cls

    @classmethod
    def intToRandColor(cls, dtype):
        dtypeStr = ValToRgba.dtypeDict[dtype]
        cls = _orthos_cpp.__dict__['IntToRandLut_%s'%dtypeStr]
        return cls

    @classmethod
    def uintSparseLut(cls, dtype):
        dtypeStr = ValToRgba.dtypeDict[dtype]
        cls = _orthos_cpp.__dict__['UIntSparseLut_%s'%dtypeStr]
        return cls


    @classmethod
    def normalize(cls, dtype, channels=None):
        dtypeStr = ValToRgba.dtypeDict[dtype]
        cls = _orthos_cpp.__dict__['NormalizedGray_%s'%dtypeStr]
        return cls

    @classmethod
    def unmodified(cls, dtype, channels=None):
        """
            only for values which naturally
            fall into the uint8 range.

            No normalization what so ever is applied,
            values are just casted to a tiny vector
            of uint8 of length 4.
        """
        pass

    @classmethod
    def labelToImplicitRandom(cls, dtype):
        pass

    @classmethod
    def sparseMappedExplicit(cls, dtype):
        pass





def makeRGBAImage(image, cppLut):
    return applyLut2D(image, cppLut)
    #sshape = image.shape[0:2]
    #imageFlat = image.reshape([sshape[0]*sshape[1],-1])
    #imageFlat = imageFlat.squeeze()
    ##print "FLAT",imageFlat.shape, imageFlat.dtype
    #imageFlatRGBA = applyLut(imageFlat, cppLut)
    #imageRGBA = imageFlatRGBA.reshape([sshape[0],sshape[1],-1])
    #return imageRGBA.squeeze()
