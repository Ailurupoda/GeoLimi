# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\districts_form.ui'
#
# Created: Mon Apr 02 13:50:47 2018
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

class Ui_districts_form(object):
    def setupUi(self, districts_form):
        districts_form.setObjectName(_fromUtf8("districts_form"))
        districts_form.resize(400, 490)
        self.verticalLayout = QtGui.QVBoxLayout(districts_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnAdd = QtGui.QPushButton(districts_form)
        self.btnAdd.setMinimumSize(QtCore.QSize(65, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8("icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnDelete = QtGui.QPushButton(districts_form)
        self.btnDelete.setEnabled(True)
        self.btnDelete.setMinimumSize(QtCore.QSize(65, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDelete.setIcon(icon1)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.horizontalLayout.addWidget(self.btnDelete)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tvdistricts = QtGui.QTableView(districts_form)
        self.tvdistricts.setObjectName(_fromUtf8("tvdistricts"))
        self.verticalLayout.addWidget(self.tvdistricts)
        self.btnQuitter = QtGui.QPushButton(districts_form)
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

        self.retranslateUi(districts_form)
        QtCore.QMetaObject.connectSlotsByName(districts_form)

    def retranslateUi(self, districts_form):
        districts_form.setWindowTitle(_translate("districts_form", "Geolimi - Districts", None))
        self.btnAdd.setToolTip(_translate("districts_form", "Ajouter un district", None))
        self.btnAdd.setText(_translate("districts_form", "Ajout", None))
        self.btnDelete.setToolTip(_translate("districts_form", "Supprimer le district", None))
        self.btnDelete.setText(_translate("districts_form", "Suppression", None))
        self.btnQuitter.setToolTip(_translate("districts_form", "Quitter la fenêtre et valider", None))
        self.btnQuitter.setText(_translate("districts_form", "Quitter", None))

