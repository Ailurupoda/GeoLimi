# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\type_activite_form.ui'
#
# Created: Mon Apr 02 13:51:02 2018
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

class Ui_type_activite_form(object):
    def setupUi(self, type_activite_form):
        type_activite_form.setObjectName(_fromUtf8("type_activite_form"))
        type_activite_form.resize(392, 636)
        self.tvType_activite = QtGui.QTableView(type_activite_form)
        self.tvType_activite.setGeometry(QtCore.QRect(10, 50, 361, 538))
        self.tvType_activite.setObjectName(_fromUtf8("tvType_activite"))
        self.btnQuitter = QtGui.QPushButton(type_activite_form)
        self.btnQuitter.setGeometry(QtCore.QRect(10, 600, 361, 30))
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
        self.layoutWidget = QtGui.QWidget(type_activite_form)
        self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 361, 32))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.horizontalLayout = QtGui.QHBoxLayout(self.layoutWidget)
        self.horizontalLayout.setMargin(0)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnAdd = QtGui.QPushButton(self.layoutWidget)
        self.btnAdd.setMinimumSize(QtCore.QSize(65, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon1)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnDelete = QtGui.QPushButton(self.layoutWidget)
        self.btnDelete.setEnabled(True)
        self.btnDelete.setMinimumSize(QtCore.QSize(65, 30))
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDelete.setIcon(icon2)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.horizontalLayout.addWidget(self.btnDelete)

        self.retranslateUi(type_activite_form)
        QtCore.QMetaObject.connectSlotsByName(type_activite_form)

    def retranslateUi(self, type_activite_form):
        type_activite_form.setWindowTitle(_translate("type_activite_form", "Geolimi - Acitivite - Ajout", None))
        type_activite_form.setToolTip(_translate("type_activite_form", "Quitter la fenêtre et valider", None))
        self.btnQuitter.setText(_translate("type_activite_form", "Quitter", None))
        self.btnAdd.setToolTip(_translate("type_activite_form", "Ajouter une nouvelle activité", None))
        self.btnAdd.setText(_translate("type_activite_form", "Ajout", None))
        self.btnDelete.setToolTip(_translate("type_activite_form", "Supprimer l\'activité", None))
        self.btnDelete.setText(_translate("type_activite_form", "Suppression", None))

