# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\cylcle_bio_form.ui'
#
# Created: Mon Apr 02 13:50:44 2018
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

class Ui_cycle_bio(object):
    def setupUi(self, cycle_bio):
        cycle_bio.setObjectName(_fromUtf8("cycle_bio"))
        cycle_bio.resize(422, 517)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(cycle_bio.sizePolicy().hasHeightForWidth())
        cycle_bio.setSizePolicy(sizePolicy)
        self.verticalLayout = QtGui.QVBoxLayout(cycle_bio)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.btnAdd = QtGui.QPushButton(cycle_bio)
        self.btnAdd.setMinimumSize(QtCore.QSize(65, 30))
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/add.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnAdd.setIcon(icon)
        self.btnAdd.setObjectName(_fromUtf8("btnAdd"))
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnDelete = QtGui.QPushButton(cycle_bio)
        self.btnDelete.setEnabled(True)
        self.btnDelete.setMinimumSize(QtCore.QSize(65, 30))
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(_fromUtf8(":/plugins/geolimi/icons/delete.png")), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnDelete.setIcon(icon1)
        self.btnDelete.setObjectName(_fromUtf8("btnDelete"))
        self.horizontalLayout.addWidget(self.btnDelete)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tvcycle_bio = QtGui.QTableView(cycle_bio)
        self.tvcycle_bio.setObjectName(_fromUtf8("tvcycle_bio"))
        self.verticalLayout.addWidget(self.tvcycle_bio)
        self.btnQuitter = QtGui.QPushButton(cycle_bio)
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

        self.retranslateUi(cycle_bio)
        QtCore.QMetaObject.connectSlotsByName(cycle_bio)

    def retranslateUi(self, cycle_bio):
        cycle_bio.setWindowTitle(_translate("cycle_bio", "Geolimi - Cycles Biologique", None))
        self.btnAdd.setToolTip(_translate("cycle_bio", "Ajouter un nouveau cycle biologique", None))
        self.btnAdd.setText(_translate("cycle_bio", "Ajout", None))
        self.btnDelete.setToolTip(_translate("cycle_bio", "Supprimer le cycle biologique", None))
        self.btnDelete.setText(_translate("cycle_bio", "Suppression", None))
        self.btnQuitter.setToolTip(_translate("cycle_bio", "Quitter la fenêtre et valider", None))
        self.btnQuitter.setText(_translate("cycle_bio", "Quitter", None))

import resourcesGeolimi_rc
