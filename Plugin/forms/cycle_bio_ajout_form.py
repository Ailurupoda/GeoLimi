# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\cycle_bio_ajout_form.ui'
#
# Created: Mon Apr 02 13:50:43 2018
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

class Ui_cycle_bio_ajout(object):
    def setupUi(self, cycle_bio_ajout):
        cycle_bio_ajout.setObjectName(_fromUtf8("cycle_bio_ajout"))
        cycle_bio_ajout.resize(465, 224)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(cycle_bio_ajout.sizePolicy().hasHeightForWidth())
        cycle_bio_ajout.setSizePolicy(sizePolicy)
        self.widget = QtGui.QWidget(cycle_bio_ajout)
        self.widget.setGeometry(QtCore.QRect(0, 0, 461, 151))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(10)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_3 = QtGui.QLabel(self.widget)
        self.label_3.setMinimumSize(QtCore.QSize(40, 0))
        self.label_3.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_3.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.horizontalLayout_2.addWidget(self.label_3)
        self.le_cycle_bio = QtGui.QLineEdit(self.widget)
        self.le_cycle_bio.setMinimumSize(QtCore.QSize(200, 0))
        self.le_cycle_bio.setObjectName(_fromUtf8("le_cycle_bio"))
        self.horizontalLayout_2.addWidget(self.le_cycle_bio)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        spacerItem = QtGui.QSpacerItem(20, 48, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.btnBox = QtGui.QDialogButtonBox(self.widget)
        self.btnBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnBox.setCenterButtons(True)
        self.btnBox.setObjectName(_fromUtf8("btnBox"))
        self.verticalLayout.addWidget(self.btnBox)
        self.label_3.setBuddy(self.le_cycle_bio)

        self.retranslateUi(cycle_bio_ajout)
        QtCore.QMetaObject.connectSlotsByName(cycle_bio_ajout)

    def retranslateUi(self, cycle_bio_ajout):
        cycle_bio_ajout.setWindowTitle(_translate("cycle_bio_ajout", "Form", None))
        self.label_3.setText(_translate("cycle_bio_ajout", "Cycle_biologique", None))

