from array_data_source_base import ArrayDataSourceBase
import vigra


class VigraChunkedArrayHdf5(ArrayDataSourceBase):
    def __init__(self, **kwargs):
        mutable = kwargs.pop('mutable',False)
        self.chunkedArray = vigra.ChunkedArrayHDF5(**kwargs)
        s = self.chunkedArray.shape
        d = self.chunkedArray.dtype
        self.dimension = len(s)
        super(VigraChunkedArrayHdf5, self).__init__(shape=s,dtype=d,
                                                    mutable=mutable)


    def __getitem__(self,key):
        return self.chunkedArray[key]


    def getData(self, spatialSlicing, t=None):
        if self.dimension == 3:
            return  self.chunkedArray[spatialSlicing]
        else:
            tslice = (slice(t,t+1),)
            slicing  = spatialSlicing + tslice
            return  self.chunkedArray[slicing]

    def commitSubarray(self,start,val):
        print start
        print val.shape, val.dtype
        self.chunkedArray.commitSubarray(start,val)

    def checkoutSubarray(self, start,stop):
        return self.chunkedArray.checkoutSubarray(start,stop)


    def flushToDisk(self):
        print "CLOSE THAT ARRAY"
        self.chunkedArray.flush()