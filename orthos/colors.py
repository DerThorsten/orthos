
#http://stackoverflow.com/questions/309149/generate-distinctly-different-rgb-colors-in-graphs
# http://phrogz.net/css/distinct-colors.html

import numpy

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
