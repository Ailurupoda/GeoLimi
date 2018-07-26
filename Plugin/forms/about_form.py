# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\about_form.ui'
#
# Created: Mon Apr 02 13:50:38 2018
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

class Ui_about_form(object):
    def setupUi(self, about_form):
        about_form.setObjectName(_fromUtf8("about_form"))
        about_form.resize(601, 690)
        about_form.setMinimumSize(QtCore.QSize(536, 352))
        self.verticalLayout = QtGui.QVBoxLayout(about_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.scrollArea = QtGui.QScrollArea(about_form)
        self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setObjectName(_fromUtf8("scrollArea"))
        self.scrollAreaWidgetContents = QtGui.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 581, 641))
        self.scrollAreaWidgetContents.setObjectName(_fromUtf8("scrollAreaWidgetContents"))
        self.verticalLayout_2 = QtGui.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.groupBox_3 = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox_3.sizePolicy().hasHeightForWidth())
        self.groupBox_3.setSizePolicy(sizePolicy)
        self.groupBox_3.setMinimumSize(QtCore.QSize(0, 75))
        self.groupBox_3.setObjectName(_fromUtf8("groupBox_3"))
        self.label = QtGui.QLabel(self.groupBox_3)
        self.label.setGeometry(QtCore.QRect(15, 22, 261, 41))
        self.label.setObjectName(_fromUtf8("label"))
        self.verticalLayout_2.addWidget(self.groupBox_3)
        self.groupBox_6 = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_6.setObjectName(_fromUtf8("groupBox_6"))
        self.verticalLayout_8 = QtGui.QVBoxLayout(self.groupBox_6)
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.gridLayout_4 = QtGui.QGridLayout()
        self.gridLayout_4.setObjectName(_fromUtf8("gridLayout_4"))
        self.label_19 = QtGui.QLabel(self.groupBox_6)
        self.label_19.setObjectName(_fromUtf8("label_19"))
        self.gridLayout_4.addWidget(self.label_19, 0, 0, 1, 1)
        self.verticalLayout_8.addLayout(self.gridLayout_4)
        self.verticalLayout_2.addWidget(self.groupBox_6)
        self.groupBox_4 = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_4.setObjectName(_fromUtf8("groupBox_4"))
        self.verticalLayout_6 = QtGui.QVBoxLayout(self.groupBox_4)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.gridLayout_3 = QtGui.QGridLayout()
        self.gridLayout_3.setObjectName(_fromUtf8("gridLayout_3"))
        self.label_15 = QtGui.QLabel(self.groupBox_4)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.gridLayout_3.addWidget(self.label_15, 0, 0, 1, 1)
        self.verticalLayout_6.addLayout(self.gridLayout_3)
        self.verticalLayout_2.addWidget(self.groupBox_4)
        self.groupBox_5 = QtGui.QGroupBox(self.scrollAreaWidgetContents)
        self.groupBox_5.setObjectName(_fromUtf8("groupBox_5"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.groupBox_5)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.label_2 = QtGui.QLabel(self.groupBox_5)
        self.label_2.setText(_fromUtf8(""))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.verticalLayout_7.addWidget(self.label_2)
        self.verticalLayout_2.addWidget(self.groupBox_5)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.verticalLayout.addWidget(self.scrollArea)
        self.buttonBox = QtGui.QDialogButtonBox(about_form)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.verticalLayout.addWidget(self.buttonBox)

        self.retranslateUi(about_form)
        QtCore.QMetaObject.connectSlotsByName(about_form)

    def retranslateUi(self, about_form):
        about_form.setWindowTitle(_translate("about_form", "GeoLimi - A propos", None))
        self.groupBox_3.setTitle(_translate("about_form", "Auteurs", None))
        self.label.setText(_translate("about_form", "Antoine BLAIN\n"
"Corentin FALCONE\n"
"Florent GRASLAND", None))
        self.groupBox_6.setTitle(_translate("about_form", "Sources", None))
        self.label_19.setText(_translate("about_form", "Dépôt sur GitHub", None))
        self.groupBox_4.setTitle(_translate("about_form", "Licence", None))
        self.label_15.setText(_translate("about_form", "Licence GPL Version 3\n"
"Personne ne doit être limité par les logiciels qu\'il utilise. Il y a quatre libertés que tout utilisateur doit posséder :\n"
"\n"
"la liberté d\'utiliser le logiciel à n\'importe quelle fin,\n"
"la liberté de modifier le programme pour répondre à ses besoins,\n"
"la liberté de redistribuer des copies à ses amis et voisins,\n"
"la liberté de partager avec d\'autres les modifications qu\'il a faites.\n"
"Quand un programme offre à ses utilisateurs toutes ces libertés, nous le qualifions de logiciel libre.", None))
        self.groupBox_5.setTitle(_translate("about_form", "Ressources", None))

