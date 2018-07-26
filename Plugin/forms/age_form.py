# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\age_form.ui'
#
# Created: Mon Apr 02 13:50:40 2018
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

class Ui_age_form(object):
    def setupUi(self, age_form):
        age_form.setObjectName(_fromUtf8("age_form"))
        age_form.resize(410, 559)
        self.verticalLayout = QtGui.QVBoxLayout(age_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnAdd = QtGui.QPushButton(age_form)
        self.btnAdd.setMinimumSize(QtCore.QSize(65, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnDelete = QtGui.QPushButton(age_form)
        self.btnDelete.setEnabled(True)
        self.btnDelete.setMinimumSize(QtCore.QSize(65, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDelete.setIcon(icon1)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.horizontalLayout.addWidget(self.btnDelete)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tvage = QtGui.QTableView(age_form)
        self.tvage.setObjectName(_fromUtf8("tvage"))
        self.verticalLayout.addWidget(self.tvage)
        self.btnQuitter = QtGui.QPushButton(age_form)
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

        self.retranslateUi(age_form)
        QtCore.QMetaObject.connectSlotsByName(age_form)

    def retranslateUi(self, age_form):
        age_form.setWindowTitle(_translate("age_form", "Geolimi - Ages", None))
        self.btnAdd.setToolTip(_translate("age_form", "Ajouter un age", None))
        self.btnAdd.setText(_translate("age_form", "Ajout", None))
        self.btnDelete.setToolTip(_translate("age_form", "Supprimer l\'age sélectionné", None))
        self.btnDelete.setText(_translate("age_form", "Suppression", None))
        self.btnQuitter.setToolTip(_translate("age_form", "Quitter la fenêtre et valider les actions", None))
        self.btnQuitter.setText(_translate("age_form", "Quitter", None))

