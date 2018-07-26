# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\ancien_logger_ajout_form.ui'
#
# Created: Mon Apr 02 13:50:41 2018
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

class Ui_ancien_logger_ajout_form(object):
    def setupUi(self, ancien_logger_ajout_form):
        ancien_logger_ajout_form.setObjectName(_fromUtf8("ancien_logger_ajout_form"))
        ancien_logger_ajout_form.resize(180, 154)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ancien_logger_ajout_form.sizePolicy().hasHeightForWidth())
        ancien_logger_ajout_form.setSizePolicy(sizePolicy)
        ancien_logger_ajout_form.setMinimumSize(QtCore.QSize(180, 154))
        ancien_logger_ajout_form.setMaximumSize(QtCore.QSize(180, 154))
        self.verticalLayout = QtGui.QVBoxLayout(ancien_logger_ajout_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(ancien_logger_ajout_form)
        self.label_3.setMinimumSize(QtCore.QSize(40, 0))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.le_anc_log = QtGui.QLineEdit(ancien_logger_ajout_form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.le_anc_log.sizePolicy().hasHeightForWidth())
        self.le_anc_log.setSizePolicy(sizePolicy)
        self.le_anc_log.setMinimumSize(QtCore.QSize(50, 0))
        self.le_anc_log.setMaximumSize(QtCore.QSize(50, 16777215))
        self.le_anc_log.setMaxLength(5)
        self.le_anc_log.setObjectName(_fromUtf8("le_anc_log"))
        self.horizontalLayout_2.addWidget(self.le_anc_log)
        spacerItem = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem1 = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem1)
        self.btnBox = QtGui.QDialogButtonBox(ancien_logger_ajout_form)
        self.btnBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnBox.setCenterButtons(True)
        self.btnBox.setObjectName(_fromUtf8("btnBox"))
        self.verticalLayout.addWidget(self.btnBox)
        self.label_3.setBuddy(self.le_anc_log)

        self.retranslateUi(ancien_logger_ajout_form)
        QtCore.QMetaObject.connectSlotsByName(ancien_logger_ajout_form)

    def retranslateUi(self, ancien_logger_ajout_form):
        ancien_logger_ajout_form.setWindowTitle(_translate("ancien_logger_ajout_form", "Geolimi - Ancien logger - Ajout", None))
        self.label_3.setText(_translate("ancien_logger_ajout_form", "Code", None))

import resourcesGeolimi_rc
