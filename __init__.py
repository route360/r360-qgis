"""
This file lets QGIS know that the folder is a Python module.

It must contain a classFactory(iface) function that QGIS will use
to initialize the plugin.
"""


def classFactory(iface):
    """Produce an instance of main plugin class.

    The interface object, iface, is the entry point to QGIS components,
    therefore the plugin should save a reference for later use.
    """
    from ggapi.plugin import Plugin
    return Plugin(iface)
