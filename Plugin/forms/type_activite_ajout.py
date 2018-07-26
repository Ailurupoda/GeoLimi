# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\type_activite_ajout.ui'
#
# Created: Mon Apr 02 13:51:01 2018
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

class Ui_type_activite_ajout_form(object):
    def setupUi(self, type_activite_ajout_form):
        type_activite_ajout_form.setObjectName(_fromUtf8("type_activite_ajout_form"))
        type_activite_ajout_form.resize(392, 175)
        self.btnBox = QtGui.QDialogButtonBox(type_activite_ajout_form)
        self.btnBox.setGeometry(QtCore.QRect(-20, 110, 407, 23))
        self.btnBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnBox.setCenterButtons(True)
        self.btnBox.setObjectName(_fromUtf8("btnBox"))
        self.layoutWidget = QtGui.QWidget(type_activite_ajout_form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 50, 341, 22))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.label_3 = QtGui.QLabel(self.layoutWidget)
        self.label_3.setMinimumSize(QtCore.QSize(40, 0))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout.addWidget(self.label_3)
        self.le_type_activite = QtGui.QLineEdit(self.layoutWidget)
        self.le_type_activite.setMinimumSize(QtCore.QSize(200, 0))
        self.le_type_activite.setObjectName(_fromUtf8("le_type_activite"))
        self.horizontalLayout.addWidget(self.le_type_activite)
        self.label_3.setBuddy(self.le_type_activite)

        self.retranslateUi(type_activite_ajout_form)
        QtCore.QMetaObject.connectSlotsByName(type_activite_ajout_form)

    def retranslateUi(self, type_activite_ajout_form):
        type_activite_ajout_form.setWindowTitle(_translate("type_activite_ajout_form", "Geolimi - Activite - Ajout", None))
        self.label_3.setText(_translate("type_activite_ajout_form", "Type d\'activité", None))

