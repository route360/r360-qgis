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

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from qgis.core import *
from qgis.utils import *
from qgis.gui import *
from combobox_handler import Combobox_handler
from plugin_part import Plugin_part
from ..ui.dist_matrix import Ui_DistM_Dialog
from ggapi.workers import Runner, DistanceMatrixWorker
from ggapi.helpers import Features, next_weekday
from ggapi import settings
from ggapi.constants import (
    FORMAT_LINEAR,
    FORMAT_STANDARD,
    FORMAT_ROUTES,
    FORMAT_LINES,
    MODE_BICYCLING,
    MODE_DRIVING,
    MODE_TRANSIT,
    MODE_WALKING,
    UNIT_METERS,
    UNIT_MINUTES
)


class Distance_matrix_dialog(QDialog, Ui_DistM_Dialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(True)


class Distance_matrix(Plugin_part):
    def __init__(self, iface):
        super(Distance_matrix, self).__init__(iface)
        self.dlg = Distance_matrix_dialog(self.mainWindow)
        self.dlg.pub_dateTimeEdit.hide()
        self.dlg.pub_deptRdo.hide()
        self.dlg.pub_arrRdo.hide()
        self.dlg.rdoPublic.hide()
        self.runner = Runner(DistanceMatrixWorker)
        self.connect()
        self.dlg_opened = False
        self.from_layer = None
        self.to_layer = None
        self.outputDir = ''
        self.output_file_spec = "CSV file (*.csv)"
        self.file_type = "CSV "
        self.layer_combobox_list = [self.dlg.inPoint1, self.dlg.inPoint2]

        self.bar = QgsMessageBar()
        self.bar.setSizePolicy( QSizePolicy.Expanding, QSizePolicy.Fixed )
        self.dlg.layout().addWidget(self.bar, 7,0, 1,0)

    def connect(self):
        self.dlg.btnFile.clicked.connect(self.set_output_path)
        self.dlg.rdoLinear.toggled.connect(self.handle_format_radio)
        self.dlg.rdoStandard.toggled.connect(self.handle_format_radio)
        self.dlg.buttonBox.accepted.connect(self.work)
        self.dlg.buttonBox.rejected.connect(self.reject)
        self.dlg.chkNearest.stateChanged.connect(self.check_k_nearest)
        self.dlg.rdoPublic.toggled.connect(self.handle_public)
        self.dlg.rdoLinear.toggled.connect(self.handle_output_type)
        self.dlg.rdoLines.toggled.connect(self.handle_output_type)
        self.dlg.rdoRoute.toggled.connect(self.handle_output_type)
        self.dlg.rdoStandard.toggled.connect(self.handle_output_type)

    def handle_output_type(self):
        if self.dlg.rdoRoute.isChecked() or self.dlg.rdoLines.isChecked():
            self.output_file_spec = "shape file (*.shp)"
            self.file_type = "SHP"
        else:
            self.output_file_spec = "CSV file (*.csv)"
            self.file_type = "CSV"
        self.outputDir = ''
        self.dlg.outFile.setText(self.outputDir)

    def handle_public(self):
        if self.dlg.rdoPublic.isChecked():
            self.dlg.pub_dateTimeEdit.setEnabled(True)
            self.dlg.pub_deptRdo.setEnabled(True)
            self.dlg.pub_arrRdo.setEnabled(True)
        else:
            self.dlg.pub_dateTimeEdit.setEnabled(False)
            self.dlg.pub_deptRdo.setEnabled(False)
            self.dlg.pub_arrRdo.setEnabled(False)

    def check_fields(self):
        if self.dlg.inPoint1.currentIndex() == -1:
            raise Exception("Please specify input point layer")
        if self.dlg.inPoint2.currentIndex() == -1:
            raise Exception("Please specify target point layer")
        if self.dlg.outFile.text() == '':
            raise Exception("Please specify output file")
        self.from_boxes.check_id_column()
        self.to_boxes.check_id_column()
        if self.get_from_layer().featureCount() * self.get_to_layer().featureCount() > settings.MAX_DISTANCE:
            raise Exception("Number of distances exceeds limit ({})".format(settings.MAX_DISTANCE))

    def check_k_nearest(self):
        if self.dlg.chkNearest.isChecked():
            self.dlg.spnNearest.setEnabled(True)
        else:
            self.dlg.spnNearest.setEnabled(False)

    def get_transport_mode(self):
        if self.dlg.rdoCar.isChecked():
            return MODE_DRIVING
        elif self.dlg.rdoBike.isChecked():
            return MODE_BICYCLING
        elif self.dlg.rdoWalk.isChecked():
            return MODE_WALKING
        elif self.dlg.rdoPublic.isChecked():
            return MODE_TRANSIT

    def get_format_mode(self):
        if self.dlg.rdoLinear.isChecked():
            return FORMAT_LINEAR
        elif self.dlg.rdoStandard.isChecked():
            return FORMAT_STANDARD
        elif self.dlg.rdoRoute.isChecked():
            return FORMAT_ROUTES
        elif self.dlg.rdoLines.isChecked():
            return FORMAT_LINES

    def get_unit_mode(self):
        if self.dlg.rdoMeter.isChecked():
            return UNIT_METERS
        elif self.dlg.rdoMinutes.isChecked():
            return UNIT_MINUTES

    def update_comboboxes(self):
        self.from_boxes = Combobox_handler(self.dlg.inPoint1, self.dlg.inPoint1label, self.dlg.inField1, self.dlg.inField1label, self.point_layer_list, self.dlg, self.bar)
        self.to_boxes = Combobox_handler(self.dlg.inPoint2, self.dlg.inPoint2label, self.dlg.inField2, self.dlg.inField2label, self.point_layer_list, self.dlg, self.bar)

    def update_ui(self):
        self.dlg.pub_dateTimeEdit.setDate(next_weekday())


    def get_from_layer(self):
        return self.from_boxes.get_layer()

    def get_to_layer(self):
        return self.to_boxes.get_layer()

    def get_from_id(self):
        return self.from_boxes.get_id()

    def get_to_id(self):
        return self.to_boxes.get_id()

    def handle_format_radio(self):
        if self.dlg.rdoLinear.isChecked():
            if not self.dlg.chkNearest.isEnabled():
                self.dlg.chkNearest.setEnabled(True)
        else:
            self.dlg.chkNearest.setEnabled(False)
            self.dlg.chkNearest.setCheckState(Qt.Unchecked)

    def get_traveltime(self):
        if self.dlg.rdoPublic.isChecked():
            if self.dlg.pub_arrRdo.isChecked():
                return "arrival_time"
            elif self.dlg.pub_deptRdo.isChecked():
                return "departure_time"
        else:
            return ""

    def get_timevalue(self):
        if self.dlg.rdoPublic.isChecked():
            return str(self.dlg.pub_dateTimeEdit.dateTime().toString("yyyy-MM-ddThh:mm"))
        else:
            return ""

    def get_routelinetype(self):
        if self.dlg.rdoLines.isChecked() or self.dlg.rdoRoute.isChecked():
            return "19"
        else:
            return "-1"

    def work(self):
        self.bar.clearWidgets()
        try:
            self.check_fields()
            self.dlg.buttonBox.button(QDialogButtonBox.Ok).setEnabled(False)
            # start the worker in a new thread
            worker = self.runner.start(fromlayer= self.get_from_layer(),
                                       tolayer= self.get_to_layer(),
                                       fromidcolumn= self.get_from_id(),
                                       toidcolumn= self.get_to_id(),
                                       format= self.get_format_mode(),
                                       outfile= self.outputDir,
                                       mode= self.get_transport_mode(),
                                       unit= self.get_unit_mode(),
                                       traveltime=self.get_traveltime(),
                                       timevalue=self.get_timevalue(),
                                       routelinetype=self.get_routelinetype(),
                                       limitnearest= self.dlg.spnNearest.value() if self.dlg.chkNearest.isChecked() else None)

            worker.finished.connect(self.handlefinished)
            worker.completed.connect(self.handlecompleted)
            worker.raised.connect(self.handleraised)
            worker.progress.connect(self.dlg.progressBar.setValue)

        except Exception as error:
            self.bar.pushWarning("Error", error.message)

    def handlefinished(self):
        self.dlg.buttonBox.button(QDialogButtonBox.Ok).setEnabled(True)
        self.dlg.progressBar.setValue(0)

    def handlecompleted(self, result):
        self.bar.clearWidgets()
        self.bar.pushSuccess("Success", "{} file complete.".format(self.file_type))
        if self.dlg.addToMap_checkBox.isChecked():
            self.iface.addVectorLayer(self.outputDir,
                                      path.basename(self.outputDir),
                                      "ogr")

    def handleraised(self, error):
        self.bar.clearWidgets()
        self.bar.pushCritical("An error occurred", error)

    def reject(self):
        self.runner.stop()
        self.dlg.reject()
