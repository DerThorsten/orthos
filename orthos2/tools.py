import numpy
from pyqtgraph.Qt import QtCore
import logging
import time

_nameToPattern = {
    'SolidPattern': QtCore.Qt.SolidPattern,
    'LinearGradientPattern': QtCore.Qt.LinearGradientPattern,
    'Dense1Pattern': QtCore.Qt.Dense1Pattern,
    'Dense2Pattern': QtCore.Qt.Dense2Pattern,
    'Dense3Pattern': QtCore.Qt.Dense3Pattern,
    'Dense4Pattern': QtCore.Qt.Dense4Pattern,
    'Dense5Pattern': QtCore.Qt.Dense5Pattern,
    'Dense6Pattern': QtCore.Qt.Dense6Pattern,
    'Dense7Pattern': QtCore.Qt.Dense7Pattern,
    'NoBrush': QtCore.Qt.NoBrush,
    'HorPattern': QtCore.Qt.HorPattern,
    'VerPattern': QtCore.Qt.VerPattern,
    'CrossPattern': QtCore.Qt.CrossPattern,
    'BDiagPattern': QtCore.Qt.BDiagPattern,
    'FDiagPattern': QtCore.Qt.FDiagPattern,
    'DiagCrossPattern': QtCore.Qt.DiagCrossPattern
}

def getQtPattern(name):
    return _nameToPattern[str(name)]


def convertRGBToHTMLColor(rgb_tuple):
    """ convert an (R, G, B) tuple to #RRGGBB """
    hexcolor = '#%02x%02x%02x' % rgb_tuple
    # that's it! '%02x' means zero-padded, 2-digit hex values
    return hexcolor




distinctiveColors13 = numpy.array([
    (255,0,0),
    (0,255,0),
    (0,0,255),
    (242,79,19),
    (255,174,13),
    (140,255,8),
    (9,64,24),
    (160,242,193),
    (17,197,242),
    (24,24,242),
    (63,8,77),
    (242,155,213)
], dtype='uint8')



def defaultAxisColor(i):
    global distinctiveColors13
    return distinctiveColors13[i]




class ScopeLogger(object):
    def __init__(self, name):
        self.name = name
    def __enter__(self):
        logging.debug("START    : %s"%self.name)
        self.t0 = time.time()
    def __exit__(self, type, value, traceback):
        self.t1 = time.time()
        dt = self.t1 - self.t0
        logging.debug("FINISHED : %s, took: %f"%(self.name,dt))
