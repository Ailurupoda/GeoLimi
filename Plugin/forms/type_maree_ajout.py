# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\type_maree_ajout.ui'
#
# Created: Mon Apr 02 13:51:03 2018
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

class Ui_type_maree_ajout(object):
    def setupUi(self, type_maree_ajout):
        type_maree_ajout.setObjectName(_fromUtf8("type_maree_ajout"))
        type_maree_ajout.resize(400, 173)
        self.btnBox = QtGui.QDialogButtonBox(type_maree_ajout)
        self.btnBox.setGeometry(QtCore.QRect(-30, 140, 407, 23))
        self.btnBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnBox.setCenterButtons(True)
        self.btnBox.setObjectName(_fromUtf8("btnBox"))
        self.layoutWidget = QtGui.QWidget(type_maree_ajout)
        self.layoutWidget.setGeometry(QtCore.QRect(20, 40, 341, 22))
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
        self.le_type_maree = QtGui.QLineEdit(self.layoutWidget)
        self.le_type_maree.setMinimumSize(QtCore.QSize(200, 0))
        self.le_type_maree.setObjectName(_fromUtf8("le_type_maree"))
        self.horizontalLayout.addWidget(self.le_type_maree)
        self.label_3.setBuddy(self.le_type_maree)

        self.retranslateUi(type_maree_ajout)
        QtCore.QMetaObject.connectSlotsByName(type_maree_ajout)

    def retranslateUi(self, type_maree_ajout):
        type_maree_ajout.setWindowTitle(_translate("type_maree_ajout", "Geolimi - Maree - Ajout", None))
        self.label_3.setText(_translate("type_maree_ajout", "Type marée", None))

