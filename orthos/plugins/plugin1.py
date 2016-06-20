from yapsy.IPlugin import IPlugin

class MyPlugin(IPlugin):
    def activate(self):
        super(MyPlugin, self).activate()
        print "I've been activated!"

    def deactivate(self):
        super(MyPlugin, self).deactivate()
        print "I've been deactivated!"
