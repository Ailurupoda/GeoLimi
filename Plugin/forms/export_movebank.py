# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\export_movebank.ui'
#
# Created: Mon Apr 02 13:50:51 2018
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

class Ui_export_movebank(object):
    def setupUi(self, export_movebank):
        export_movebank.setObjectName(_fromUtf8("export_movebank"))
        export_movebank.resize(450, 200)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(export_movebank.sizePolicy().hasHeightForWidth())
        export_movebank.setSizePolicy(sizePolicy)
        export_movebank.setMinimumSize(QtCore.QSize(450, 100))
        export_movebank.setMaximumSize(QtCore.QSize(450, 200))
        self.verticalLayout = QtGui.QVBoxLayout(export_movebank)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout = QtGui.QHBoxLayout()
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.lbl_chemin = QtGui.QLabel(export_movebank)
        self.lbl_chemin.setMinimumSize(QtCore.QSize(300, 0))
        self.lbl_chemin.setMaximumSize(QtCore.QSize(16777215, 30))
        self.lbl_chemin.setStyleSheet(_fromUtf8("background-color: rgb(209, 223, 245);"))
        self.lbl_chemin.setObjectName(_fromUtf8("lbl_chemin"))
        self.horizontalLayout.addWidget(self.lbl_chemin)
        spacerItem = QtGui.QSpacerItem(58, 17, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pb_recherche = QtGui.QPushButton(export_movebank)
        self.pb_recherche.setMinimumSize(QtCore.QSize(30, 30))
        self.pb_recherche.setMaximumSize(QtCore.QSize(30, 30))
        self.pb_recherche.setObjectName(_fromUtf8("pb_recherche"))
        self.horizontalLayout.addWidget(self.pb_recherche)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.rb_periode = QtGui.QRadioButton(export_movebank)
        self.rb_periode.setObjectName(_fromUtf8("rb_periode"))
        self.horizontalLayout_2.addWidget(self.rb_periode)
        self.label = QtGui.QLabel(export_movebank)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_2.addWidget(self.label)
        self.dteDebut = QtGui.QDateEdit(export_movebank)
        self.dteDebut.setCalendarPopup(True)
        self.dteDebut.setObjectName(_fromUtf8("dteDebut"))
        self.horizontalLayout_2.addWidget(self.dteDebut)
        self.label_2 = QtGui.QLabel(export_movebank)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_2.addWidget(self.label_2)
        self.dteFin = QtGui.QDateEdit(export_movebank)
        self.dteFin.setCalendarPopup(True)
        self.dteFin.setObjectName(_fromUtf8("dteFin"))
        self.horizontalLayout_2.addWidget(self.dteFin)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.rb_zone = QtGui.QRadioButton(export_movebank)
        self.rb_zone.setChecked(False)
        self.rb_zone.setObjectName(_fromUtf8("rb_zone"))
        self.horizontalLayout_3.addWidget(self.rb_zone)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.pb_movebank = QtGui.QProgressBar(export_movebank)
        self.pb_movebank.setProperty("value", 0)
        self.pb_movebank.setObjectName(_fromUtf8("pb_movebank"))
        self.verticalLayout.addWidget(self.pb_movebank)
        self.gridLayout = QtGui.QGridLayout()
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.pb_export = QtGui.QPushButton(export_movebank)
        self.pb_export.setObjectName(_fromUtf8("pb_export"))
        self.gridLayout.addWidget(self.pb_export, 0, 0, 1, 1)
        self.pb_quitter = QtGui.QPushButton(export_movebank)
        self.pb_quitter.setObjectName(_fromUtf8("pb_quitter"))
        self.gridLayout.addWidget(self.pb_quitter, 0, 1, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)

        self.retranslateUi(export_movebank)
        QtCore.QMetaObject.connectSlotsByName(export_movebank)

    def retranslateUi(self, export_movebank):
        export_movebank.setWindowTitle(_translate("export_movebank", "Geolimi - Export Movebank", None))
        self.lbl_chemin.setText(_translate("export_movebank", "chemin du fichier", None))
        self.pb_recherche.setToolTip(_translate("export_movebank", "Choix du chemin où enregistrer le fichier exporté", None))
        self.pb_recherche.setText(_translate("export_movebank", "...", None))
        self.rb_periode.setText(_translate("export_movebank", "Export par periode", None))
        self.label.setText(_translate("export_movebank", "Début", None))
        self.label_2.setText(_translate("export_movebank", "Fin", None))
        self.rb_zone.setText(_translate("export_movebank", "Export total", None))
        self.pb_export.setToolTip(_translate("export_movebank", "Exporter les données de la base pour movebank", None))
        self.pb_export.setText(_translate("export_movebank", "Export", None))
        self.pb_quitter.setToolTip(_translate("export_movebank", "Sortir de la fenêtre", None))
        self.pb_quitter.setText(_translate("export_movebank", "Quitter", None))

