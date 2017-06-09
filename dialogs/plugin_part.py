# -*- coding: utf-8 -*-

from PyQt4.QtGui import *
import os, sys
from qgis.core import *
from ggapi.constants import COUNTRY_DICT
from ggapi.settings import COUNTRY

class Plugin_part(object):
    def __init__(self, iface):
        self.iface = iface
        self.mainWindow = self.iface.mainWindow()
        self.point_layer_list = []

    def show_dialog(self):
        if self.dlg_opened == False:
            self.add_point_layers()
            self.update_comboboxes()
            self.update_ui()
            self.dlg.setWindowTitle(self.dlg.windowTitle()+" ("+COUNTRY_DICT[COUNTRY]+")")
            self.dlg.show()
            self.dlg_opened = True

    def add_point_layers(self):
        layers = self.iface.legendInterface().layers()
        for layer in layers:
            layerType = layer.type()
            if layerType == QgsMapLayer.VectorLayer and layer.geometryType() == QGis.Point:
                self.point_layer_list.append(layer)


    def set_output_path(self):
        self.outputDir = QFileDialog.getSaveFileName(self.dlg, u'Choose folder for output', os.path.splitdrive(sys.executable)[0]+ '\\', self.output_file_spec)
        if not self.outputDir == '':
            self.outputDir = self.outputDir.replace('\\','/')
            self.dlg.outFile.setText(self.outputDir)