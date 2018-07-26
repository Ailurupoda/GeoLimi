# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\espece.ui'
#
# Created: Mon Mar 12 09:27:29 2018
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

class Ui_espece(object):
    def setupUi(self, espece):
        espece.setObjectName(_fromUtf8("espece"))
        espece.resize(418, 330)
        self.pb_supprimer_espece = QtGui.QPushButton(espece)
        self.pb_supprimer_espece.setGeometry(QtCore.QRect(300, 179, 41, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pb_supprimer_espece.setFont(font)
        self.pb_supprimer_espece.setStyleSheet(_fromUtf8("background-color: rgb(255, 84, 84);"))
        self.pb_supprimer_espece.setObjectName(_fromUtf8("pb_supprimer_espece"))
        self.pb_ajout_espece = QtGui.QPushButton(espece)
        self.pb_ajout_espece.setGeometry(QtCore.QRect(300, 89, 41, 41))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.pb_ajout_espece.setFont(font)
        self.pb_ajout_espece.setStyleSheet(_fromUtf8("background-color: rgb(141, 255, 65);"))
        self.pb_ajout_espece.setObjectName(_fromUtf8("pb_ajout_espece"))
        self.lbl_ajout_espece = QtGui.QLabel(espece)
        self.lbl_ajout_espece.setGeometry(QtCore.QRect(300, 70, 94, 16))
        self.lbl_ajout_espece.setObjectName(_fromUtf8("lbl_ajout_espece"))
        self.lbl_supprimer_espece = QtGui.QLabel(espece)
        self.lbl_supprimer_espece.setGeometry(QtCore.QRect(300, 160, 111, 16))
        self.lbl_supprimer_espece.setObjectName(_fromUtf8("lbl_supprimer_espece"))
        self.widget = QtGui.QWidget(espece)
        self.widget.setGeometry(QtCore.QRect(23, 42, 258, 213))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.lbl_liste_espece = QtGui.QLabel(self.widget)
        self.lbl_liste_espece.setStyleSheet(_fromUtf8("background-color: rgb(255, 255, 127);"))
        self.lbl_liste_espece.setObjectName(_fromUtf8("lbl_liste_espece"))
        self.verticalLayout.addWidget(self.lbl_liste_espece)
        self.lw_espece = QtGui.QListWidget(self.widget)
        self.lw_espece.setEditTriggers(QtGui.QAbstractItemView.DoubleClicked|QtGui.QAbstractItemView.EditKeyPressed|QtGui.QAbstractItemView.SelectedClicked)
        self.lw_espece.setObjectName(_fromUtf8("lw_espece"))
        item = QtGui.QListWidgetItem()
        item.setFlags(QtCore.Qt.ItemIsSelectable|QtCore.Qt.ItemIsEditable|QtCore.Qt.ItemIsDragEnabled|QtCore.Qt.ItemIsUserCheckable|QtCore.Qt.ItemIsEnabled)
        self.lw_espece.addItem(item)
        self.verticalLayout.addWidget(self.lw_espece)

        self.retranslateUi(espece)
        QtCore.QMetaObject.connectSlotsByName(espece)

    def retranslateUi(self, espece):
        espece.setWindowTitle(_translate("espece", "Dialog", None))
        self.pb_supprimer_espece.setText(_translate("espece", "-", None))
        self.pb_ajout_espece.setText(_translate("espece", "+", None))
        self.lbl_ajout_espece.setText(_translate("espece", "Ajouter une espèce", None))
        self.lbl_supprimer_espece.setText(_translate("espece", "Supprimer une espèce", None))
        self.lbl_liste_espece.setText(_translate("espece", "Liste des espèces dans la base:", None))
        __sortingEnabled = self.lw_espece.isSortingEnabled()
        self.lw_espece.setSortingEnabled(False)
        item = self.lw_espece.item(0)
        item.setText(_translate("espece", "Ligne_editable + QWidget ou LW ? Nom FR ou Nom Latin ? ", None))
        self.lw_espece.setSortingEnabled(__sortingEnabled)

