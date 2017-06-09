# -*- coding: utf-8 -*-
"""Main plugin class

This class represents the main plugin. It
"""

# Import the PyQt and QGIS libraries
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
# Initialize Qt resources from file resources.py
import resources
# Import the code for the dialogs
from ggapi.dialogs import Distance_matrix, POI_distance, Servicearea, Manager
from ggapi import settings

ICON = ":/plugins/ggapi/icon.png"
ICON_KEY = ":/plugins/ggapi/icon_key.png"
ICON_SERVICEAREA = ":/plugins/ggapi/icon_servicearea.png"
ICON_POI = ":/plugins/ggapi/icon_POI.png"
ICON_MATRIX = ":/plugins/ggapi/icon_matrix.png"


class Plugin:
    """Gis Group API QGIS Plugin.
    """
    def __init__(self, iface):
        """Initialize the plugin.

        The interface object, iface, is passed to the plugin, so that it can
        access QGIS afterwards. This method saves a reference to iface, and
        initializes other variables used in other functions of the plugin.
        """
        self.iface = iface
        self.dlg = None

    def initGui(self):
        """Set up the plugin's GUI within QGIS.

        Sets up actions, and adds buttons and menu items that trigger them.
        """
        # Create QActions that will be used to start the plugin
        self.action_distance = QAction(QIcon(ICON_MATRIX),
                                       u"Distance Matrix...",
                                       self.iface.mainWindow())
        self.action_poi_dist = QAction(QIcon(ICON_POI),
                                       u"Distance to POI...",
                                       self.iface.mainWindow())
        self.action_servicearea = QAction(QIcon(ICON_SERVICEAREA),
                                          u"Service area...",
                                          self.iface.mainWindow())
        self.action_manager = QAction(QIcon(ICON_KEY),
                                      u"Manage key",
                                      self.iface.mainWindow())

        # connect actions to the run() methods via QObject (the base Qt object)
        self.action_distance.triggered.connect(self.exec_distance_matrix)
        self.action_poi_dist.triggered.connect(self.exec_poi_dist)
        self.action_servicearea.triggered.connect(self.exec_servicearea)
        self.action_manager.triggered.connect(self.exec_manager)

        # Add menu item that triggers the action
        self.iface.addPluginToMenu(u"&ggapi", self.action_poi_dist)
        self.iface.addPluginToMenu(u"&ggapi", self.action_distance)
        self.iface.addPluginToMenu(u"&ggapi", self.action_servicearea)
        self.iface.addPluginToMenu(u"&ggapi", self.action_manager)

        if (settings.DEBUG):
            self.iface.addToolBarIcon(self.action_distance)
            self.iface.addToolBarIcon(self.action_poi_dist)
            self.iface.addToolBarIcon(self.action_servicearea)
            self.iface.addToolBarIcon(self.action_manager)
            self.show_msglog()

    def show_msglog(self):
        log = self.iface.mainWindow().findChild(QDockWidget, "MessageLog")
        log.setVisible(True)

    def unload(self):
        """This method will be run by QGis when closed.

        Removes any plugin widgets (buttons, menus, etc) from the QGIS GUI.
        """
        self.cleaning()

        # Remove the plugin menu item and icon
        self.iface.removePluginMenu(u"&ggapi", self.action_distance)
        self.iface.removePluginMenu(u"&ggapi", self.action_poi_dist)
        self.iface.removePluginMenu(u"&ggapi", self.action_servicearea)
        self.iface.removePluginMenu(u"&ggapi", self.action_manager)

        if (settings.DEBUG):
            self.iface.removeToolBarIcon(self.action_distance)
            self.iface.removeToolBarIcon(self.action_poi_dist)
            self.iface.removeToolBarIcon(self.action_servicearea)
            self.iface.removeToolBarIcon(self.action_manager)

    def exec_distance_matrix(self):
        self.dialog = Distance_matrix(self.iface)
        self.dialog.show_dialog()

    def exec_poi_dist(self):
        self.dialog = POI_distance(self.iface)
        self.dialog.show_dialog()

    def exec_servicearea(self):
        self.dialog = Servicearea(self.iface)
        self.dialog.show_dialog()

    def exec_manager(self):
        self.dialog = Manager(self.iface)
        self.dialog.show_dialog()

    def cleaning(self):
        """used when dialog is closed."""
        pass

    def test(self, text="Plugin test funktion triggered"):
        QMessageBox.information(self.iface.mainWindow(), "Test", text)
