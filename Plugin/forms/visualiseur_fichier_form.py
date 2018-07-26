# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\visualiseur_fichier_form.ui'
#
# Created: Mon Apr 02 13:51:07 2018
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

class Ui_fichier_visualiseur_form(object):
    def setupUi(self, fichier_visualiseur_form):
        fichier_visualiseur_form.setObjectName(_fromUtf8("fichier_visualiseur_form"))
        fichier_visualiseur_form.resize(400, 591)
        self.verticalLayout = QtGui.QVBoxLayout(fichier_visualiseur_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.btnAdd = QtGui.QPushButton(fichier_visualiseur_form)
        self.btnAdd.setMinimumSize(QtCore.QSize(65, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.gridLayout.addWidget(self.btnAdd, 0, 0, 1, 1)
        self.btnDelete = QtGui.QPushButton(fichier_visualiseur_form)
        self.btnDelete.setEnabled(True)
        self.btnDelete.setMinimumSize(QtCore.QSize(65, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDelete.setIcon(icon1)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.gridLayout.addWidget(self.btnDelete, 0, 1, 1, 1)
        self.tv_visualiseur_fichier = QtGui.QTableView(fichier_visualiseur_form)
        self.tv_visualiseur_fichier.setObjectName(_fromUtf8("tv_visualiseur_fichier"))
        self.gridLayout.addWidget(self.tv_visualiseur_fichier, 1, 0, 1, 2)
        self.btnQuitter = QtGui.QPushButton(fichier_visualiseur_form)
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
        self.gridLayout.addWidget(self.btnQuitter, 2, 0, 1, 2)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(fichier_visualiseur_form)
        QtCore.QMetaObject.connectSlotsByName(fichier_visualiseur_form)

    def retranslateUi(self, fichier_visualiseur_form):
        fichier_visualiseur_form.setWindowTitle(_translate("fichier_visualiseur_form", "Geolimi - Fichiers insérés", None))
        self.btnAdd.setToolTip(_translate("fichier_visualiseur_form", "Ajouter un fichier", None))
        self.btnAdd.setText(_translate("fichier_visualiseur_form", "Ajout", None))
        self.btnDelete.setToolTip(_translate("fichier_visualiseur_form", "Supprimer le fichier", None))
        self.btnDelete.setText(_translate("fichier_visualiseur_form", "Suppression", None))
        self.btnQuitter.setToolTip(_translate("fichier_visualiseur_form", "Quitter la fenêtre et valider", None))
        self.btnQuitter.setText(_translate("fichier_visualiseur_form", "Quitter", None))

import resourcesGeolimi_rc
