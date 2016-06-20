from pyqtgraph.Qt import QtGui, QtCore

class ToggleEye( QtGui.QLabel ):
    activeChanged = QtCore.Signal(bool)

    def __init__( self, parent=None ):
        super(ToggleEye, self).__init__( parent=parent )
        self._active = True
        self._eye_open = QtGui.QPixmap(":icons/icons/stock-eye-20.png")
        self._eye_closed = QtGui.QPixmap(":icons/icons/stock-eye-20-gray.png")
        self.setPixmap(self._eye_open)

    def active( self ):
        return self._active

    def setActive( self, b ):
        if b == self._active:
            return
        self._active = b
        if b:
            self.setPixmap(self._eye_open)
        else:
            self.setPixmap(self._eye_closed)

    def toggle( self ):
        if self.active():
            self.setActive( False )
        else:
            self.setActive( True )

    def mousePressEvent( self, ev ):
        self.toggle()
        self.activeChanged.emit( self._active )

