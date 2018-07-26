# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\espece_form.ui'
#
# Created: Mon Apr 02 13:50:49 2018
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

class Ui_espece_form(object):
    def setupUi(self, espece_form):
        espece_form.setObjectName(_fromUtf8("espece_form"))
        espece_form.resize(374, 600)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(espece_form.sizePolicy().hasHeightForWidth())
        espece_form.setSizePolicy(sizePolicy)
        espece_form.setMinimumSize(QtCore.QSize(374, 600))
        espece_form.setMaximumSize(QtCore.QSize(16777215, 16777215))
        self.verticalLayout = QtGui.QVBoxLayout(espece_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnAdd = QtGui.QPushButton(espece_form)
        self.btnAdd.setMinimumSize(QtCore.QSize(65, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnDelete = QtGui.QPushButton(espece_form)
        self.btnDelete.setEnabled(True)
        self.btnDelete.setMinimumSize(QtCore.QSize(65, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDelete.setIcon(icon1)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.horizontalLayout.addWidget(self.btnDelete)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tvEspece = QtGui.QTableView(espece_form)
        self.tvEspece.setObjectName(_fromUtf8("tvEspece"))
        self.verticalLayout.addWidget(self.tvEspece)
        self.btnQuitter = QtGui.QPushButton(espece_form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.btnQuitter.sizePolicy().hasHeightForWidth())
        self.btnQuitter.setSizePolicy(sizePolicy)
        self.btnQuitter.setMinimumSize(QtCore.QSize(75, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/quit.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnQuitter.setIcon(icon2)
        self.btnQuitter.setObjectName(_fromUtf8("btnQuitter"))
        self.verticalLayout.addWidget(self.btnQuitter)

        self.retranslateUi(espece_form)
        QtCore.QMetaObject.connectSlotsByName(espece_form)

    def retranslateUi(self, espece_form):
        espece_form.setWindowTitle(_translate("espece_form", "Geolimi - Espèce", None))
        self.btnAdd.setToolTip(_translate("espece_form", "Ajouter une espèce", None))
        self.btnAdd.setText(_translate("espece_form", "Ajout", None))
        self.btnDelete.setToolTip(_translate("espece_form", "Supprimer l\'espèce", None))
        self.btnDelete.setText(_translate("espece_form", "Suppression", None))
        self.btnQuitter.setToolTip(_translate("espece_form", "Quitter la fenêtre et valider", None))
        self.btnQuitter.setText(_translate("espece_form", "Quitter", None))

import resourcesGeolimi_rc
