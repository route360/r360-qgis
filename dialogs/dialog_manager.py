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

from PyQt4.QtGui import *
from PyQt4.QtCore import *

from ..ui.manager import  Ui_Manager_dialog

class Manager_dialog(QDialog,  Ui_Manager_dialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.setupUi(self)
        self.setModal(True)

class Manager(object):
    def __init__(self, iface):
        self.iface = iface
        self.mainWindow = self.iface.mainWindow()
        self.dlg = Manager_dialog(self.mainWindow)
        self.dlg_opened = False
        self.settings = QSettings()
        self.key = self.settings.value("ggapi/test_key_1", "")
        self.dlg.lineEdit.setText(self.key)
        self.connect()

    def connect(self):
        self.dlg.buttonBox.accepted.connect(self.update_key)

    def update_key(self):
        text = self.dlg.lineEdit.text()
        self.settings.setValue("ggapi/test_key_1", text)


    def show_dialog(self):
        if self.dlg_opened == False:
            self.dlg.show()
            self.dlg_opened = True