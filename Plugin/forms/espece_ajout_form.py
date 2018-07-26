# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\espece_ajout_form.ui'
#
# Created: Mon Apr 02 13:50:48 2018
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

class Ui_espece_ajout_form(object):
    def setupUi(self, espece_ajout_form):
        espece_ajout_form.setObjectName(_fromUtf8("espece_ajout_form"))
        espece_ajout_form.resize(425, 154)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(espece_ajout_form.sizePolicy().hasHeightForWidth())
        espece_ajout_form.setSizePolicy(sizePolicy)
        espece_ajout_form.setMinimumSize(QtCore.QSize(310, 154))
        espece_ajout_form.setMaximumSize(QtCore.QSize(16777215, 154))
        self.verticalLayout = QtGui.QVBoxLayout(espece_ajout_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(espece_ajout_form)
        self.label_3.setMinimumSize(QtCore.QSize(40, 0))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.le_esp_nomfr = QtGui.QLineEdit(espece_ajout_form)
        self.le_esp_nomfr.setMinimumSize(QtCore.QSize(200, 0))
        self.le_esp_nomfr.setObjectName(_fromUtf8("le_esp_nomfr"))
        self.horizontalLayout_2.addWidget(self.le_esp_nomfr)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setSpacing(10)
        self.horizontalLayout_3.setContentsMargins(19, -1, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_4 = QtGui.QLabel(espece_ajout_form)
        self.label_4.setMinimumSize(QtCore.QSize(40, 0))
        self.label_4.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_4.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.horizontalLayout_3.addWidget(self.label_4)
        self.le_esp_nom_latin = QtGui.QLineEdit(espece_ajout_form)
        self.le_esp_nom_latin.setEnabled(True)
        self.le_esp_nom_latin.setMinimumSize(QtCore.QSize(200, 0))
        self.le_esp_nom_latin.setObjectName(_fromUtf8("le_esp_nom_latin"))
        self.horizontalLayout_3.addWidget(self.le_esp_nom_latin)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btnBox = QtGui.QDialogButtonBox(espece_ajout_form)
        self.btnBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnBox.setCenterButtons(True)
        self.btnBox.setObjectName(_fromUtf8("btnBox"))
        self.verticalLayout.addWidget(self.btnBox)
        self.label_3.setBuddy(self.le_esp_nomfr)
        self.label_4.setBuddy(self.le_esp_nomfr)

        self.retranslateUi(espece_ajout_form)
        QtCore.QMetaObject.connectSlotsByName(espece_ajout_form)

    def retranslateUi(self, espece_ajout_form):
        espece_ajout_form.setWindowTitle(_translate("espece_ajout_form", "Geolimi - Espèce - Ajout", None))
        self.label_3.setText(_translate("espece_ajout_form", "Nom français", None))
        self.label_4.setText(_translate("espece_ajout_form", "Nom latin", None))

import resourcesGeolimi_rc
