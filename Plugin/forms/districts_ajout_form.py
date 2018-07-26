# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\districts_ajout_form.ui'
#
# Created: Mon Apr 02 13:50:45 2018
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

class Ui_district_ajout_form(object):
    def setupUi(self, district_ajout_form):
        district_ajout_form.setObjectName(_fromUtf8("district_ajout_form"))
        district_ajout_form.resize(400, 181)
        self.verticalLayout_2 = QtGui.QVBoxLayout(district_ajout_form)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(district_ajout_form)
        self.label_3.setMinimumSize(QtCore.QSize(40, 0))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.le_district = QtGui.QLineEdit(district_ajout_form)
        self.le_district.setMinimumSize(QtCore.QSize(200, 0))
        self.le_district.setObjectName(_fromUtf8("le_district"))
        self.horizontalLayout_2.addWidget(self.le_district)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btnBox = QtGui.QDialogButtonBox(district_ajout_form)
        self.btnBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnBox.setCenterButtons(True)
        self.btnBox.setObjectName(_fromUtf8("btnBox"))
        self.verticalLayout.addWidget(self.btnBox)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label_3.setBuddy(self.le_district)

        self.retranslateUi(district_ajout_form)
        QtCore.QMetaObject.connectSlotsByName(district_ajout_form)

    def retranslateUi(self, district_ajout_form):
        district_ajout_form.setWindowTitle(_translate("district_ajout_form", "Form", None))
        self.label_3.setText(_translate("district_ajout_form", "Districts", None))

