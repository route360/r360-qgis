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

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from os import path

import json
from qgis.core import *
from qgis.utils import *
from qgis.gui import *
from combobox_handler import Combobox_handler
from plugin_part import Plugin_part
from ..ui.servicearea import Ui_Servicearea_Dialog
from ggapi.workers import Runner, ServiceAreaWorker
from ggapi.helpers import Features, next_weekday
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
from osgeo import ogr


class Servicearea_dialog(QDialog, Ui_Servicearea_Dialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(True)

class Servicearea(Plugin_part):
    def __init__(self, iface):
        super(Servicearea, self).__init__(iface)
        self.dlg = Servicearea_dialog(self.mainWindow)
        self.dlg.bike_lineEdit.setPlaceholderText("Bicycle speed in km/h (standard is 15 km/h)")
        self.dlg.walk_lineEdit.setPlaceholderText("Walking speed in km/h (standard is 5 km/h)")
        self.runner = Runner(ServiceAreaWorker)
        self.connect()
        self.dlg_opened = False
        self.layer = None
        self.outputDir = ''
        self.output_file_spec = "Shape file (*.shp)"
        self.layer_combobox_list = [self.dlg.inPoint]

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        self.dlg.layout().addWidget(self.bar, 6,0, 1,0)

    def check_fields(self):
        if self.dlg.inPoint.currentIndex() == -1:
            raise Exception("Please specify point layer")
        if self.dlg.outFile.text() == '':
            raise Exception("Please specify output file")
        self.boxes.check_id_column()

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
        self.dlg.bufferEdit.editingFinished.connect(self.handle_buffer)
        self.dlg.rdoPublic.toggled.connect(self.handle_public)
        self.dlg.rdoBike.toggled.connect(self.handle_bike)
        self.dlg.rdoWalk.toggled.connect(self.handle_walk)

    def handle_buffer(self):
        text = self.dlg.bufferEdit.text()
        if text == "":
            self.dlg.bufferEdit.setText("0")

    def handle_public(self):
        if self.dlg.rdoPublic.isChecked():
            self.dlg.timeEdit.setEnabled(True)
            self.dlg.date_comboBox.setEnabled(True)
            #self.dlg.pub_deptRdo.setEnabled(True)
            #self.dlg.pub_arrRdo.setEnabled(True)
        else:
            self.dlg.timeEdit.setEnabled(False)
            self.dlg.date_comboBox.setEnabled(False)
            #self.dlg.pub_deptRdo.setEnabled(False)
            #self.dlg.pub_arrRdo.setEnabled(False)

    def handle_bike(self):
        if self.dlg.rdoBike.isChecked():
            self.dlg.bike_lineEdit.setEnabled(True)
        else:
            self.dlg.bike_lineEdit.setEnabled(False)

    def handle_walk(self):
        if self.dlg.rdoWalk.isChecked():
            self.dlg.walk_lineEdit.setEnabled(True)
        else:
            self.dlg.walk_lineEdit.setEnabled(False)


    def get_transport_mode(self):
        if self.dlg.rdoCar.isChecked():
            return MODE_DRIVING
        elif self.dlg.rdoBike.isChecked():
            return MODE_BICYCLING
        elif self.dlg.rdoWalk.isChecked():
            return MODE_WALKING
        elif self.dlg.rdoPublic.isChecked():
            return MODE_TRANSIT

    def update_comboboxes(self):
        self.boxes = Combobox_handler(self.dlg.inPoint, self.dlg.inPointlabel, self.dlg.inField, self.dlg.inFieldlabel, self.point_layer_list, self.dlg, self.bar)

    def update_ui(self):
        # self.dlg.pub_dateTimeEdit.setDate(next_weekday())
        pass

    def get_layer(self):
        return self.boxes.get_layer()

    def get_id(self):
        return self.boxes.get_id()

    def get_buffer(self):
        try:
            return float(self.dlg.bufferEdit.text())
        except:
            raise Exception(u"Buffer is not set to valid value.")

    def get_date(self):
        # return int(self.dlg.pub_dateTimeEdit.dateTime().toString("yyyyMMdd"))
        date_dict = {u"Monday": 20160919,
                    u"Tuesday": 20160920,
                    u"Wednesday": 20160921,
                    u"Thursday": 20160922,
                    u"Friday": 20160923,
                    u"Saturday": 20160924,
                    u"Sunday": 20160925}
        return date_dict[unicode(self.dlg.date_comboBox.currentText())]

    def get_time(self):
        # hour = int(self.dlg.pub_dateTimeEdit.dateTime().toString("h"))
        # minute = int(self.dlg.pub_dateTimeEdit.dateTime().toString("m"))
        hour = int(self.dlg.timeEdit.dateTime().toString("h"))
        minute = int(self.dlg.timeEdit.dateTime().toString("m"))

        return 60*60*hour + 60*minute

    def get_bike_speed(self):
        if self.dlg.bike_lineEdit.text() != '':
            return int(self.dlg.bike_lineEdit.text())
        else:
            return None

    def get_walk_speed(self):
        if self.dlg.walk_lineEdit.text() != '':
            return int(self.dlg.walk_lineEdit.text())
        else:
            return None


    def work(self):
        self.bar.clearWidgets()
        try:
            self.check_fields()

            id_field_idx = self.get_id()
            layer = self.get_layer()
            id_field = layer.pendingFields()[id_field_idx]

            worker = self.runner.start(features=Features.fromlayer(self.get_layer()),
                                       idcolumn=self.get_id(),
                                       idfield=id_field,
                                       radii=self.get_times_as_list(),
                                       mode=self.get_transport_mode(),
                                       outfile=self.outputDir,
                                       buffer=self.get_buffer(),
                                       date=self.get_date(),
                                       time=self.get_time(),
                                       bike_speed = self.get_bike_speed(),
                                       walk_speed = self.get_walk_speed())

            # start the worker in a new thread
            worker.progress.connect(self.dlg.progressBar.setValue)
            worker.finished.connect(self.handlefinished)
            worker.completed.connect(self.handlecompleted)
            worker.raised.connect(self.handleraised)

        except Exception as error:
            self.bar.pushWarning("Fejl", error.message)

    def handlefinished(self):
        self.dlg.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.dlg.progressBar.setValue(0)

    def handleraised(self, error):
        self.bar.clearWidgets()
        self.bar.pushCritical("An error occurred", error)

    def handlecompleted(self, result):
        if result is not None:
            self.bar.clearWidgets()
            self.bar.pushSuccess("Success", "Service area(s) constructed.")
        if self.dlg.addToMap_checkBox.isChecked():
            self.iface.addVectorLayer(self.outputDir, path.basename(self.outputDir), "ogr")

    def reject(self):
        self.runner.stop()
        self.dlg.reject()

    def get_times_as_list(self):
        try:
            times_list = []
            text = self.dlg.lineEdit_times.text()
            for time in text.split(';'):
                if float(time) <= 120:
                    times_list.append(float(time))
                else:
                    raise Exception
            return times_list
        except:
            raise Exception("Please format times correctly.\nOnly numbers and ; are allowed.\nThe highest allowed time is 120.")
