# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\export_logger.ui'
#
# Created: Mon Apr 02 13:50:50 2018
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

class Ui_export_logger(object):
    def setupUi(self, export_logger):
        export_logger.setObjectName(_fromUtf8("export_logger"))
        export_logger.resize(450, 150)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(export_logger.sizePolicy().hasHeightForWidth())
        export_logger.setSizePolicy(sizePolicy)
        export_logger.setMinimumSize(QtCore.QSize(450, 150))
        export_logger.setMaximumSize(QtCore.QSize(450, 150))
        self.verticalLayout = QtGui.QVBoxLayout(export_logger)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_chemin = QtGui.QLabel(export_logger)
        self.lbl_chemin.setMinimumSize(QtCore.QSize(300, 0))
        self.lbl_chemin.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lbl_chemin.setStyleSheet(_fromUtf8("background-color: rgb(209, 223, 245);"))
        self.lbl_chemin.setObjectName(_fromUtf8("lbl_chemin"))
        self.horizontalLayout.addWidget(self.lbl_chemin)
        spacerItem = QtGui.QSpacerItem(58, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_recherche = QtGui.QPushButton(export_logger)
        self.pb_recherche.setMinimumSize(QtCore.QSize(30, 30))
        self.pb_recherche.setMaximumSize(QtCore.QSize(30, 30))
        self.pb_recherche.setObjectName(_fromUtf8("pb_recherche"))
        self.horizontalLayout.addWidget(self.pb_recherche)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.cb_liste = QtGui.QComboBox(export_logger)
        self.cb_liste.setObjectName(_fromUtf8("cb_liste"))
        self.cb_liste.addItem(_fromUtf8(""))
        self.verticalLayout.addWidget(self.cb_liste)
        self.pb_logger = QtGui.QProgressBar(export_logger)
        self.pb_logger.setProperty("value", 0)
        self.pb_logger.setObjectName(_fromUtf8("pb_logger"))
        self.verticalLayout.addWidget(self.pb_logger)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pb_quitter = QtGui.QPushButton(export_logger)
        self.pb_quitter.setObjectName(_fromUtf8("pb_quitter"))
        self.gridLayout.addWidget(self.pb_quitter, 1, 1, 1, 1)
        self.pb_export = QtGui.QPushButton(export_logger)
        self.pb_export.setObjectName(_fromUtf8("pb_export"))
        self.gridLayout.addWidget(self.pb_export, 1, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(export_logger)
        QtCore.QMetaObject.connectSlotsByName(export_logger)

    def retranslateUi(self, export_logger):
        export_logger.setWindowTitle(_translate("export_logger", "Geolimi - Export Logger - Form", None))
        self.lbl_chemin.setText(_translate("export_logger", "chemin du fichier", None))
        self.pb_recherche.setToolTip(_translate("export_logger", "Choix du chemin où enregistrer le fichier exporté", None))
        self.pb_recherche.setText(_translate("export_logger", "...", None))
        self.cb_liste.setToolTip(_translate("export_logger", "Sélection du district de trie pour l\'export", None))
        self.cb_liste.setItemText(0, _translate("export_logger", "Liste des districts", None))
        self.pb_quitter.setToolTip(_translate("export_logger", "Sortir de la fenêtre", None))
        self.pb_quitter.setText(_translate("export_logger", "Quitter", None))
        self.pb_export.setToolTip(_translate("export_logger", "Exporter les informations de la base dans un fichier", None))
        self.pb_export.setText(_translate("export_logger", "Export", None))

