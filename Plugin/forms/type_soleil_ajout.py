# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\type_soleil_ajout.ui'
#
# Created: Mon Apr 02 13:51:05 2018
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

class Ui_type_soleil_ajout(object):
    def setupUi(self, type_soleil_ajout):
        type_soleil_ajout.setObjectName(_fromUtf8("type_soleil_ajout"))
        type_soleil_ajout.resize(400, 171)
        self.btnBox = QtGui.QDialogButtonBox(type_soleil_ajout)
        self.btnBox.setGeometry(QtCore.QRect(0, 120, 407, 23))
        self.btnBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnBox.setCenterButtons(True)
        self.btnBox.setObjectName(_fromUtf8("btnBox"))
        self.layoutWidget = QtGui.QWidget(type_soleil_ajout)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 30, 361, 22))
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
        self.le_type_soleil = QtGui.QLineEdit(self.layoutWidget)
        self.le_type_soleil.setMinimumSize(QtCore.QSize(200, 0))
        self.le_type_soleil.setObjectName(_fromUtf8("le_type_soleil"))
        self.horizontalLayout.addWidget(self.le_type_soleil)
        self.label_3.setBuddy(self.le_type_soleil)

        self.retranslateUi(type_soleil_ajout)
        QtCore.QMetaObject.connectSlotsByName(type_soleil_ajout)

    def retranslateUi(self, type_soleil_ajout):
        type_soleil_ajout.setWindowTitle(_translate("type_soleil_ajout", "Geolimi - Soleil - Ajout", None))
        self.label_3.setText(_translate("type_soleil_ajout", "Type soleil", None))

