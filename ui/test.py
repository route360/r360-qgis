# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'ggapi/ui/test.ui'
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

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.setWindowModality(QtCore.Qt.NonModal)
        Dialog.resize(382, 497)
        Dialog.setSizeGripEnabled(True)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.vboxlayout = QtGui.QVBoxLayout()
        self.vboxlayout.setObjectName(_fromUtf8("vboxlayout"))
        self.label_4 = QtGui.QLabel(Dialog)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.vboxlayout.addWidget(self.label_4)
        self.inPoint1 = QtGui.QComboBox(Dialog)
        self.inPoint1.setObjectName(_fromUtf8("inPoint1"))
        self.vboxlayout.addWidget(self.inPoint1)
        self.gridLayout.addLayout(self.vboxlayout, 0, 0, 1, 2)
        self.vboxlayout1 = QtGui.QVBoxLayout()
        self.vboxlayout1.setObjectName(_fromUtf8("vboxlayout1"))
        self.label_6 = QtGui.QLabel(Dialog)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.vboxlayout1.addWidget(self.label_6)
        self.inField1 = QtGui.QComboBox(Dialog)
        self.inField1.setObjectName(_fromUtf8("inField1"))
        self.vboxlayout1.addWidget(self.inField1)
        self.gridLayout.addLayout(self.vboxlayout1, 1, 0, 1, 2)
        self.vboxlayout2 = QtGui.QVBoxLayout()
        self.vboxlayout2.setObjectName(_fromUtf8("vboxlayout2"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.vboxlayout2.addWidget(self.label_3)
        self.inPoint2 = QtGui.QComboBox(Dialog)
        self.inPoint2.setObjectName(_fromUtf8("inPoint2"))
        self.vboxlayout2.addWidget(self.inPoint2)
        self.gridLayout.addLayout(self.vboxlayout2, 2, 0, 1, 2)
        self.vboxlayout3 = QtGui.QVBoxLayout()
        self.vboxlayout3.setObjectName(_fromUtf8("vboxlayout3"))
        self.label_5 = QtGui.QLabel(Dialog)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.vboxlayout3.addWidget(self.label_5)
        self.inField2 = QtGui.QComboBox(Dialog)
        self.inField2.setObjectName(_fromUtf8("inField2"))
        self.vboxlayout3.addWidget(self.inField2)
        self.gridLayout.addLayout(self.vboxlayout3, 3, 0, 1, 2)
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.gridlayout = QtGui.QGridLayout(self.groupBox_2)
        self.gridlayout.setObjectName(_fromUtf8("gridlayout"))
        self.rdoLinear = QtGui.QRadioButton(self.groupBox_2)
        self.rdoLinear.setChecked(True)
        self.rdoLinear.setObjectName(_fromUtf8("rdoLinear"))
        self.gridlayout.addWidget(self.rdoLinear, 0, 0, 1, 1)
        self.rdoStandard = QtGui.QRadioButton(self.groupBox_2)
        self.rdoStandard.setObjectName(_fromUtf8("rdoStandard"))
        self.gridlayout.addWidget(self.rdoStandard, 1, 0, 1, 1)
        self.rdoSummary = QtGui.QRadioButton(self.groupBox_2)
        self.rdoSummary.setObjectName(_fromUtf8("rdoSummary"))
        self.gridlayout.addWidget(self.rdoSummary, 2, 0, 1, 2)
        self.chkNearest = QtGui.QCheckBox(self.groupBox_2)
        self.chkNearest.setObjectName(_fromUtf8("chkNearest"))
        self.gridlayout.addWidget(self.chkNearest, 3, 0, 1, 1)
        self.spnNearest = QtGui.QSpinBox(self.groupBox_2)
        self.spnNearest.setEnabled(False)
        self.spnNearest.setMinimum(1)
        self.spnNearest.setMaximum(9999)
        self.spnNearest.setObjectName(_fromUtf8("spnNearest"))
        self.gridlayout.addWidget(self.spnNearest, 3, 1, 1, 1)
        self.gridLayout.addWidget(self.groupBox_2, 4, 0, 1, 2)
        spacerItem = QtGui.QSpacerItem(20, 16, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.gridLayout.addItem(spacerItem, 5, 0, 1, 1)
        self.vboxlayout4 = QtGui.QVBoxLayout()
        self.vboxlayout4.setObjectName(_fromUtf8("vboxlayout4"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.vboxlayout4.addWidget(self.label_2)
        self.hboxlayout = QtGui.QHBoxLayout()
        self.hboxlayout.setObjectName(_fromUtf8("hboxlayout"))
        self.outFile = QtGui.QLineEdit(Dialog)
        self.outFile.setReadOnly(True)
        self.outFile.setObjectName(_fromUtf8("outFile"))
        self.hboxlayout.addWidget(self.outFile)
        self.btnFile = QtGui.QPushButton(Dialog)
        self.btnFile.setObjectName(_fromUtf8("btnFile"))
        self.hboxlayout.addWidget(self.btnFile)
        self.vboxlayout4.addLayout(self.hboxlayout)
        self.gridLayout.addLayout(self.vboxlayout4, 6, 0, 1, 2)
        self.progressBar = QtGui.QProgressBar(Dialog)
        self.progressBar.setProperty("value", 0)
        self.progressBar.setAlignment(QtCore.Qt.AlignCenter)
        self.progressBar.setTextVisible(True)
        self.progressBar.setObjectName(_fromUtf8("progressBar"))
        self.gridLayout.addWidget(self.progressBar, 7, 0, 1, 1)
        self.buttonBox_2 = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox_2.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox_2.setStandardButtons(QtGui.QDialogButtonBox.Close|QtGui.QDialogButtonBox.Ok)
        self.buttonBox_2.setObjectName(_fromUtf8("buttonBox_2"))
        self.gridLayout.addWidget(self.buttonBox_2, 7, 1, 1, 1)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox_2, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox_2, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.close)
        QtCore.QObject.connect(self.chkNearest, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.spnNearest.setEnabled)
        QtCore.QObject.connect(self.rdoStandard, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.chkNearest.setDisabled)
        QtCore.QObject.connect(self.rdoStandard, QtCore.SIGNAL(_fromUtf8("toggled(bool)")), self.spnNearest.setDisabled)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Create Distance Matrix", None))
        self.label_4.setText(_translate("Dialog", "Input point layer", None))
        self.label_6.setText(_translate("Dialog", "Input unique ID field", None))
        self.label_3.setText(_translate("Dialog", "Target point layer", None))
        self.label_5.setText(_translate("Dialog", "Target unique ID field", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Output matrix type", None))
        self.rdoLinear.setText(_translate("Dialog", "Linear (N*k x 3) distance matrix", None))
        self.rdoStandard.setText(_translate("Dialog", "Standard (N x T) distance matrix", None))
        self.rdoSummary.setText(_translate("Dialog", "Summary distance matrix (mean, std. dev., min, max)", None))
        self.chkNearest.setText(_translate("Dialog", "Use only the nearest (k) target points", None))
        self.label_2.setText(_translate("Dialog", "Output distance matrix", None))
        self.btnFile.setText(_translate("Dialog", "Browse", None))

