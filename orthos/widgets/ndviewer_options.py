import pyqtgraph as pg
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.parametertree.parameterTypes as pTypes
from pyqtgraph.parametertree import Parameter, ParameterTree, ParameterItem, registerParameterType



class NdViewerOptions(QtCore.QObject):
    
    ##
    ## @brief      { constructor_description }
    ##
    ## @param      self      { parameter_description }
    ## @param      ndViewer  { parameter_description }
    ##
    def __init__(self, ndViewer):


        super(NdViewerOptions, self).__init__()

        self.qtSettings = QtCore.QSettings('ndViewer_setttings','settings')
        self.ndViewer = ndViewer


        useOpenGl = self.qtSettings.value('Use OpenGL',True).toBool()
        useAA = self.qtSettings.value('Use Anti-Aliasing',False).toBool()
        pattern = self.qtSettings.value('bg-type','LinearGradientPattern').toString()

        params = [
            {'name': 'Global Options', 'type': 'group', 'children': [
                {'name': 'Use OpenGL', 'type': 'bool', 'value': useOpenGl, 'tip': "can lead to speedups if enabled"},
                {'name': 'Use Anti-Aliasing', 'type': 'bool', 'value': useAA},
            ]},
            {'name': 'ViewBox Options', 'type': 'group', 'children': [
                {'name': 'ViewBox Background', 'type': 'group', 'children': [
                    {
                        'name': 'bg-type', 'type': 'list', 'values': 
                        [
                            'SolidPattern',
                            'LinearGradientPattern',
                            'Dense1Pattern',
                            'Dense2Pattern',
                            'Dense3Pattern',
                            'Dense4Pattern',
                            'Dense5Pattern',
                            'Dense6Pattern',
                            'Dense7Pattern',
                            'NoBrush',
                            'HorPattern',
                            'VerPattern',
                            'CrossPattern',
                            'BDiagPattern',
                            'FDiagPattern',
                            'DiagCrossPattern'
                        ], 
                        'value': pattern
                    },
                    {'name': 'bg-color 1', 'type': 'color', 'value': (180,)*3, 'tip': "background color 1"},
                    {'name': 'bg-color 2', 'type': 'color', 'value': (60 ,)*3, 'tip': "background color 2"},
                ]},
                {'name': 'Show Axis', 'type': 'bool', 'value': False},
            ]},
            {'name': 'Save/Restore functionality', 'type': 'group', 'children': [
                {'name': 'Save State', 'type': 'action'},
                {'name': 'Restore State', 'type': 'action', 'children': [
                    {'name': 'Add missing items', 'type': 'bool', 'value': True},
                    {'name': 'Remove extra items', 'type': 'bool', 'value': True},
                ]},
            ]}
        ]

        ## Create tree of Parameter objects
        self.p = Parameter.create(name='params', type='group', children=params)
        self.p.param('Save/Restore functionality', 'Save State').sigActivated.connect(self.save)
        self.p.param('Save/Restore functionality', 'Restore State').sigActivated.connect(self.restore)



        # Too lazy for recursion:
        for child in self.p.children():
            child.sigValueChanged.connect(self._valueChanging)
            for ch2 in child.children():
                ch2.sigValueChanged.connect(self._valueChanging)
                for ch3 in ch2.children():
                    ch3.sigValueChanged.connect(self._valueChanging)

    def _valueChanging(self, param, value):
        print "Value changing (not finalized): %s %s" % (param, value)
        self.qtSettings.setValue(param.name(), value)
        self.qtSettings.sync()

    def __getitem__(self,key):
        """ get value of parameter"""
        return self.p[key]
    def param(self, *args, **kwargs):
        """ get the param object"""
        return self.p.param(*args,**kwargs)

    def save(self):
        state = self.p.saveState()
        print type(state)
    def restore(self):
        global state
        add = self.p['Save/Restore functionality', 'Restore State', 'Add missing items']
        rem = self.p['Save/Restore functionality', 'Restore State', 'Remove extra items']
        self.p.restoreState(state, addChildren=add, removeChildren=rem)
