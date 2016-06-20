from yapsy.PluginManager import PluginManager
import logging 
logging.basicConfig(level=logging.DEBUG)

def main():   
    # Load the plugins from the plugin directory.
    manager = PluginManager()
    manager.setPluginPlaces(["orthos/plugins"])
    manager.collectPlugins()

    # Loop round the plugins and print their names.
    for plugin in manager.getAllPlugins():
        print "Fo"
        plugin.plugin_object.print_name()

if __name__ == "__main__":
    print "done"
