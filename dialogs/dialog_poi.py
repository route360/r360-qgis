# -*- coding: utf-8 -*-
#-----------------------------------------------------------
# Copyright (C) 2014  Gis Group Aps
#-----------------------------------------------------------
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
#---------------------------------------------------------------------

from os import path
from PyQt4.QtCore import *
from PyQt4.QtGui import *

from qgis.core import *
from qgis.utils import *
from qgis.gui import *
from combobox_handler import Combobox_handler
from plugin_part import Plugin_part
from ..ui.poi_dist import Ui_ClosestPOI_Dialog
from ggapi.workers import Runner, POIWorker
from ggapi.helpers import Features
from ggapi.constants import (
    FORMAT_LINEAR,
    FORMAT_STANDARD,
    MODE_BICYCLING,
    MODE_DRIVING,
    MODE_TRANSIT,
    MODE_WALKING,
    UNIT_METERS,
    UNIT_MINUTES
)
from ggapi.settings import COUNTRY, MAX_POI_COUNT

class POI_distance_dialog(QDialog, Ui_ClosestPOI_Dialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(True)


class POI_distance(Plugin_part):
    def __init__(self, iface):
        super(POI_distance, self).__init__(iface)
        self.dlg = POI_distance_dialog(self.mainWindow)
        self.runner = Runner(POIWorker)
        self.connect()
        self.dlg_opened = False
        self.layer = None
        self.outputDir = ''
        self.output_file_spec = "CSV file (*.csv)"
        self.layer_combobox_list = [self.dlg.inPoint]

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        self.dlg.layout().addWidget(self.bar, 7,0, 1,0)

    def check_fields(self):
        if self.dlg.inPoint.currentIndex() == -1:
            raise Exception("Please specify point layer")
        if self.dlg.outFile.text() == '':
            raise Exception("Please specify output file")
        if len(self.create_poi_list()) == 0:
            raise Exception("Please specify at least one POI type")
        self.boxes.check_id_column()
        if self.get_layer().featureCount() > MAX_POI_COUNT:
            raise Exception("Feature count of layer exceeds limit of {}".format(MAX_POI_COUNT))

    def handle_layer(self):
        idx = self.dlg.inPoint.currentIndex()
        self.layer = self.point_layer_list[idx]
        self.dlg.inField.clear()
        for f in self.layer.pendingFields():
            self.dlg.inField.addItem(f.name())

    def connect(self):
        self.dlg.inPoint.currentIndexChanged.connect(self.handle_layer)
        self.dlg.btnFile.clicked.connect(self.set_output_path)
        self.dlg.buttonBox.accepted.connect(self.work)
        self.dlg.buttonBox.rejected.connect(self.reject)
        self.dlg.checkBox_custom.toggled.connect(self.toggle_custom_layer)

    def toggle_custom_layer(self):
        if self.dlg.checkBox_custom.isChecked():
            self.custom_boxes.setEnabled(True)
        else:
            self.custom_boxes.setEnabled(False)

    def get_transport_mode(self):
        if self.dlg.rdoCar.isChecked():
            return MODE_DRIVING
        elif self.dlg.rdoBike.isChecked():
            return MODE_BICYCLING
        elif self.dlg.rdoWalk.isChecked():
            return MODE_WALKING
#        elif self.dlg.rdoPublic.isChecked():
#            return MODE_TRANSIT

    def update_comboboxes(self):
        self.boxes = Combobox_handler(self.dlg.inPoint, self.dlg.inPointlabel, self.dlg.inField, self.dlg.inFieldlabel, self.point_layer_list, self.dlg, self.bar)
        self.custom_boxes = Combobox_handler(self.dlg.POIlayer, self.dlg.POIlayerlabel, self.dlg.POIfield, self.dlg.POIfieldlabel, self.point_layer_list, self.dlg, self.bar)

    def update_ui(self):
        if COUNTRY == "DENMARK":
            pass
            self.custom_boxes.setEnabled(False)
        else:
            self.dlg.groupBox_POI_boxes.setVisible(False)


    def get_layer(self):
        return self.boxes.get_layer()

    def get_id(self):
        return self.boxes.get_id()

    def create_poi_list(self):
        poi_list = []
        if self.dlg.checkBox_library.isChecked():
            poi_list.append("library")
        if self.dlg.checkBox_doctor.isChecked():
            poi_list.append("doctor")
        if self.dlg.checkBox_train.isChecked():
            poi_list.append("train")
        if self.dlg.checkBox_airport.isChecked():
            poi_list.append("airport")
        if self.dlg.checkBox_daycare.isChecked():
            poi_list.append("daycare")
        if self.dlg.checkBox_pharmacy.isChecked():
            poi_list.append("pharmacy")
        if self.dlg.checkBox_junction.isChecked():
            poi_list.append("junction")
        if self.dlg.checkBox_hospital.isChecked():
            poi_list.append("hospital")
        if self.dlg.checkBox_school.isChecked():
            poi_list.append("school")
        if self.dlg.checkBox_forest.isChecked():
            poi_list.append("forest")
        if self.dlg.checkBox_coast.isChecked():
            poi_list.append("coast")
        if self.dlg.checkBox_metro.isChecked():
            poi_list.append("metro")
        if self.dlg.checkBox_strain.isChecked():
            poi_list.append("strain")
        if self.dlg.checkBox_stop.isChecked():
            poi_list.append("stop")
        if self.dlg.checkBox_supermarket.isChecked():
            poi_list.append("supermarket")
        if self.dlg.checkBox_lake.isChecked():
            poi_list.append("lake")
        return poi_list

    def work(self):
        self.bar.clearWidgets()
        try:
            self.check_fields()
            worker = self.runner.start(features=Features.fromlayer(self.get_layer()),
                                       idcolumn=self.get_id(),
                                       pois=self.create_poi_list(),
                                       outfile=self.outputDir,
                                       mode=self.get_transport_mode())

            # start the worker in a new thread
            worker.finished.connect(self.handlefinished)
            worker.completed.connect(self.handlecompleted)
            worker.raised.connect(self.handleraised)
            worker.progress.connect(self.dlg.progressBar.setValue)

        except Exception as error:
            self.bar.pushWarning("Fejl", error.message)

    def handlefinished(self):
        self.dlg.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.dlg.progressBar.setValue(0)


    def handlecompleted(self, result):
        self.bar.clearWidgets()
        self.bar.pushSuccess("Success", "CSV file complete.")
        if self.dlg.addToMap_checkBox.isChecked():
            self.iface.addVectorLayer(self.outputDir, path.basename(self.outputDir), "ogr")

    def handleraised(self, error):
        self.bar.clearWidgets()
        self.bar.pushCritical("An error occurred", error)

    def reject(self):
        self.runner.stop()
        self.dlg.reject()
