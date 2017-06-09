# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ggapi/ui/ggapi.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
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

class Ui_GGAPI(object):
    def setupUi(self, GGAPI):
        GGAPI.setObjectName(_fromUtf8("GGAPI"))
        GGAPI.resize(504, 415)
        self.verticalLayout = QtGui.QVBoxLayout(GGAPI)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.buttonBox = QtGui.QDialogButtonBox(GGAPI)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(GGAPI)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), GGAPI.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), GGAPI.reject)
        QtCore.QMetaObject.connectSlotsByName(GGAPI)

    def retranslateUi(self, GGAPI):
        GGAPI.setWindowTitle(_translate("GGAPI", "XxXx", None))

