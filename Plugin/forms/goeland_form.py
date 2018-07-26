# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\goeland_form.ui'
#
# Created: Mon Apr 02 13:50:52 2018
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

class Ui_goeland(object):
    def setupUi(self, goeland):
        goeland.setObjectName(_fromUtf8("goeland"))
        goeland.resize(641, 497)
        self.verticalLayout = QtGui.QVBoxLayout(goeland)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.label = QtGui.QLabel(goeland)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout.addWidget(self.label)
        self.tv_goeland = QtGui.QTableView(goeland)
        self.tv_goeland.setObjectName(_fromUtf8("tv_goeland"))
        self.verticalLayout.addWidget(self.tv_goeland)
        self.btnQuitter = QtGui.QPushButton(goeland)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnQuitter.sizePolicy().hasHeightForWidth())
        self.btnQuitter.setSizePolicy(sizePolicy)
        self.btnQuitter.setMinimumSize(QtCore.QSize(75, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/quit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnQuitter.setIcon(icon)
        self.btnQuitter.setObjectName(_fromUtf8("btnQuitter"))
        self.verticalLayout.addWidget(self.btnQuitter)

        self.retranslateUi(goeland)
        QtCore.QMetaObject.connectSlotsByName(goeland)

    def retranslateUi(self, goeland):
        goeland.setWindowTitle(_translate("goeland", "Form", None))
        self.label.setText(_translate("goeland", "Visualiseur des fichiers Goelands", None))
        self.btnQuitter.setText(_translate("goeland", "Quitter", None))

import resourcesGeolimi_rc
