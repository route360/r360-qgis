# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\GG\2015-10-05_bitbucket_api_plugin\qgisgroup\ggapi\ui\manager.ui'
#
# Created: Mon Sep 12 11:29:12 2016
#      by: PyQt4 UI code generator 4.10.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Manager_dialog(object):
    def setupUi(self, Manager_dialog):
        Manager_dialog.setObjectName(_fromUtf8("Manager_dialog"))
        Manager_dialog.setWindowModality(QtCore.Qt.NonModal)
        Manager_dialog.resize(390, 119)
        Manager_dialog.setSizeGripEnabled(True)
        self.verticalLayout = QtGui.QVBoxLayout(Manager_dialog)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(Manager_dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.lineEdit = QtGui.QLineEdit(Manager_dialog)
        self.lineEdit.setObjectName(_fromUtf8("lineEdit"))
        self.verticalLayout.addWidget(self.lineEdit)
        spacerItem = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.buttonBox = QtGui.QDialogButtonBox(Manager_dialog)
        self.buttonBox.setEnabled(True)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(Manager_dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Manager_dialog.close)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Manager_dialog.close)
        QtCore.QMetaObject.connectSlotsByName(Manager_dialog)

    def retranslateUi(self, Manager_dialog):
        Manager_dialog.setWindowTitle(_translate("Manager_dialog", "Manager", None))
        self.label.setText(_translate("Manager_dialog", "Key", None))

