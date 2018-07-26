# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\load_data_form.ui'
#
# Created: Mon Apr 02 13:50:59 2018
#      by: PyQt4 UI code generator 4.11.3
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

class Ui_load_data_form(object):
    def setupUi(self, load_data_form):
        load_data_form.setObjectName(_fromUtf8("load_data_form"))
        load_data_form.resize(410, 200)
        load_data_form.setMinimumSize(QtCore.QSize(410, 200))
        load_data_form.setMaximumSize(QtCore.QSize(410, 200))
        self.verticalLayout_6 = QtGui.QVBoxLayout(load_data_form)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.groupBox_5 = QtGui.QGroupBox(load_data_form)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_3.setContentsMargins(-1, -1, 25, -1)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_12 = QtGui.QLabel(self.groupBox_5)
        self.label_12.setMaximumSize(QtCore.QSize(70, 16777215))
        self.label_12.setObjectName(_fromUtf8("label_12"))
        self.horizontalLayout_4.addWidget(self.label_12)
        self.cmbTheme = QtGui.QComboBox(self.groupBox_5)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.cmbTheme.sizePolicy().hasHeightForWidth())
        self.cmbTheme.setSizePolicy(sizePolicy)
        self.cmbTheme.setObjectName(_fromUtf8("cmbTheme"))
        self.horizontalLayout_4.addWidget(self.cmbTheme)
        self.verticalLayout_3.addLayout(self.horizontalLayout_4)
        self.verticalLayout_6.addWidget(self.groupBox_5)
        self.btnCharger = QtGui.QPushButton(load_data_form)
        self.btnCharger.setMinimumSize(QtCore.QSize(0, 30))
        self.btnCharger.setObjectName(_fromUtf8("btnCharger"))
        self.verticalLayout_6.addWidget(self.btnCharger)
        self.pbProcess = QtGui.QProgressBar(load_data_form)
        self.pbProcess.setProperty("value", 0)
        self.pbProcess.setObjectName(_fromUtf8("pbProcess"))
        self.verticalLayout_6.addWidget(self.pbProcess)
        self.bboxFermer = QtGui.QDialogButtonBox(load_data_form)
        self.bboxFermer.setMinimumSize(QtCore.QSize(0, 20))
        self.bboxFermer.setStandardButtons(QtGui.QDialogButtonBox.Close)
        self.bboxFermer.setObjectName(_fromUtf8("bboxFermer"))
        self.verticalLayout_6.addWidget(self.bboxFermer)

        self.retranslateUi(load_data_form)
        QtCore.QMetaObject.connectSlotsByName(load_data_form)

    def retranslateUi(self, load_data_form):
        load_data_form.setWindowTitle(_translate("load_data_form", "Geolimi - Chargement de données", None))
        self.groupBox_5.setToolTip(_translate("load_data_form", "Charger les données de la base dans QGIS", None))
        self.groupBox_5.setTitle(_translate("load_data_form", "Styles à appliquer", None))
        self.label_12.setText(_translate("load_data_form", "Thème", None))
        self.cmbTheme.setToolTip(_translate("load_data_form", "Charger les données de la base dans QGIS", None))
        self.btnCharger.setToolTip(_translate("load_data_form", "Charger les données de la base dans QGIS", None))
        self.btnCharger.setText(_translate("load_data_form", "Charger les données", None))
        self.pbProcess.setToolTip(_translate("load_data_form", "Charger les données de la base dans QGIS", None))

