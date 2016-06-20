import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
from pyqtgraph.dockarea import *
from pyqtgraph.dockarea.Dock import DockLabel
from pyqtgraph.dockarea.DockArea import *
import types

from .. tools import convertRGBToHTMLColor


# TODO 
# - colors are not propagated if maximized
# - two docklabels appear (one is ColorDockLabel,other is DockLabel)
#   (if maximized for instance)
class ColorDockArea(DockArea):
    def __init__(self,*args,**kwargs):
        super(ColorDockArea,self).__init__(*args,**kwargs)
        self.dockList  = []
        self.storedLayout = None
    def clear(self):
        docks = self.findAll()[1]
        for dock in docks.values():
            print "CLOSE DOCK"
            if False:#dock.closable:
                dock.close()
            else:
                self.home.moveDock(dock, "top", None)

    def addTempArea(self):
        if self.home is None:
            area = DockArea(temporary=True, home=self)
            self.tempAreas.append(area)
            win = TempAreaWindow(area)
            win.setWindowFlags(QtCore.Qt.WindowMinimizeButtonHint)
            area.win = win
            win.show()
        else:
            area = self.home.addTempArea()
        #print "added temp area", area, area.window()
        return area


    def onClose(self):
        for t in self.tempAreas:
            t.win.close()
            t.close()

    def maximizeViewerDock(self, dock):
        state = self.saveState()
        assert dock.isViewerDock
        # apparently we need to first move all docks
        # below the maximized dock
        # and then move the dock above them
        # seems like one of them is superfluous 
        # but both are needed
        # 
        # TODO identifying the docks via
        # name seems ugly (but should work)
        for d in self.dockList:
            if d.isViewerDock and d.name != dock.name:
                self.moveDock(d,'below',dock)
                self.moveDock(dock,'above',d)
        return state

    def addDockToViewer(self, dock=None, position='bottom', relativeTo=None, **kwds):
        print "FOOO"
        super(ColorDockArea, self).addDock(dock=dock,position=position,relativeTo=relativeTo,**kwds)
        dock.mainArea = self
        self.dockList.append(dock)

    def restoreStoredLayout(self):
        if self.storedLayout is not None:
            self.restoreState(self.storedLayout)

class ColorDock(Dock):


    def __init__(self,color,*args,**kwargs):
        super(ColorDock,self).__init__(*args,**kwargs)
        # overwrite color docks label
        #self.label = ColorDockLabel(self.name(), self, False)
        self.buttons = [QtGui.QToolButton(self.label) for x in range(4)]
        self.isViewerDock = False

        #self.label.sigMaximizedClicked.connect(self.onMaximizeClicked)
        #self.label.sigRestoreClicked.connect(self.onRestoreLayout)
        #self.label.sigButtonClick3.connect(self.sig_button_click_3)
        
        def labelUpdateStyle(self):
            r = '3px'
            if self.dim:
                fg = '#aaa'
                bg = convertRGBToHTMLColor(color)
                border = '#339'
            else:
                fg = '#fff'
                bg = convertRGBToHTMLColor(color)
                border = '#55B'
            
            if self.orientation == 'vertical':
                self.vStyle = """DockLabel { 
                    background-color : %s; 
                    color : %s; 
                    border-top-right-radius: 0px; 
                    border-top-left-radius: %s; 
                    border-bottom-right-radius: 0px; 
                    border-bottom-left-radius: %s; 
                    border-width: 0px; 
                    border-right: 2px solid %s;
                    padding-top: 3px;
                    padding-bottom: 3px;
                }""" % (bg, fg, r, r, border)
                self.setStyleSheet(self.vStyle)
            else:
                self.hStyle = """DockLabel { 
                    background-color : %s; 
                    color : %s; 
                    border-top-right-radius: %s; 
                    border-top-left-radius: %s; 
                    border-bottom-right-radius: 0px; 
                    border-bottom-left-radius: 0px; 
                    border-width: 0px; 
                    border-bottom: 2px solid %s;
                    padding-left: 3px;
                    padding-right: 3px;
                }""" % (bg, fg, r, r, border)
                self.setStyleSheet(self.hStyle)

        method = types.MethodType(labelUpdateStyle, self.label)
        self.label.updateStyle = method
        self.label.updateStyle()

    def onMaximizeClicked(self):
        print "maximize"
        self.mainArea.maximizeViewerDock(self)

    def onRestoreLayout(self):
        self.mainArea.restoreStoredLayout()


class ColorDockLabel(DockLabel):

    sigMaximizedClicked = QtCore.Signal()
    sigRestoreClicked = QtCore.Signal()
    sigButtonClick3 = QtCore.Signal()
    sigButtonClick4 = QtCore.Signal()

    def __init__(self, text, dock, showCloseButton):
        super(ColorDockLabel, self).__init__(text, dock, showCloseButton)
        #view-fullscreen
        self.buttons = [QtGui.QToolButton(self) for x in range(4)]
        self.buttons[0].setIcon(QtGui.QIcon.fromTheme("view-fullscreen"))
        self.buttons[0].clicked.connect(self.sigMaximizedClicked)

        self.buttons[1].setIcon(QtGui.QIcon.fromTheme("view-restore"))
        self.buttons[1].clicked.connect(self.sigRestoreClicked)
        

        self.buttons[2].setIcon(QtGui.QIcon.fromTheme("zoom-fit-best"))  
        self.buttons[2].clicked.connect(self.sigButtonClick3)

        self.buttons[3].setIcon(QtGui.QIcon.fromTheme("zoom-original"))  
        self.buttons[3].clicked.connect(self.sigButtonClick4)




    def resizeEvent(self, ev):

       # if self.Button1:
       #     if self.orientation == 'vertical':
       #         size = ev.size().width()
       #         pos = QtCore.QPoint(0, ev.size().height() - size)
       #     else:
       #         size = ev.size().height()
       #         pos = QtCore.QPoint(0, 0)
       #     self.button1.setFixedSize(QtCore.QSize(size, size))
       #     self.button1.move(pos)
       if self.buttons:
           for i in range(0, len(self.buttons)):
               if self.orientation == 'vertical':
                   size = ev.size().width()
                   pos = QtCore.QPoint(0, ev.size().height() - i*size - size)
               else:
                   size = ev.size().height()
                   pos = QtCore.QPoint(i*size, 0)
               self.buttons[i].setFixedSize(QtCore.QSize(size, size))
               self.buttons[i].move(pos)
       super(ColorDockLabel, self).resizeEvent(ev)
