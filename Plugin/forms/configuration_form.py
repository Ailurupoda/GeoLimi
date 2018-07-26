# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'forms\configuration_form.ui'
#
# Created: Mon Apr 02 13:50:42 2018
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

class Ui_configuration_form(object):
    def setupUi(self, configuration_form):
        configuration_form.setObjectName(_fromUtf8("configuration_form"))
        configuration_form.resize(400, 280)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(configuration_form.sizePolicy().hasHeightForWidth())
        configuration_form.setSizePolicy(sizePolicy)
        configuration_form.setMinimumSize(QtCore.QSize(400, 280))
        configuration_form.setMaximumSize(QtCore.QSize(400, 280))
        self.verticalLayout = QtGui.QVBoxLayout(configuration_form)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.groupBox = QtGui.QGroupBox(configuration_form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Fixed, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.groupBox.sizePolicy().hasHeightForWidth())
        self.groupBox.setSizePolicy(sizePolicy)
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.formLayout = QtGui.QFormLayout(self.groupBox)
        self.formLayout.setFieldGrowthPolicy(QtGui.QFormLayout.AllNonFixedFieldsGrow)
        self.formLayout.setObjectName(_fromUtf8("formLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setContentsMargins(78, -1, -1, -1)
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.label_5 = QtGui.QLabel(self.groupBox)
        self.label_5.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_5.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName(_fromUtf8("label_5"))
        self.horizontalLayout_2.addWidget(self.label_5)
        self.leHote = QtGui.QLineEdit(self.groupBox)
        self.leHote.setMinimumSize(QtCore.QSize(222, 0))
        self.leHote.setObjectName(_fromUtf8("leHote"))
        self.horizontalLayout_2.addWidget(self.leHote)
        self.formLayout.setLayout(0, QtGui.QFormLayout.LabelRole, self.horizontalLayout_2)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(80, -1, -1, -1)
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.label_6 = QtGui.QLabel(self.groupBox)
        self.label_6.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_6.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName(_fromUtf8("label_6"))
        self.horizontalLayout_3.addWidget(self.label_6)
        self.lePort = QtGui.QLineEdit(self.groupBox)
        self.lePort.setMinimumSize(QtCore.QSize(54, 0))
        self.lePort.setObjectName(_fromUtf8("lePort"))
        self.horizontalLayout_3.addWidget(self.lePort)
        self.formLayout.setLayout(1, QtGui.QFormLayout.LabelRole, self.horizontalLayout_3)
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setContentsMargins(37, -1, -1, -1)
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.label_7 = QtGui.QLabel(self.groupBox)
        self.label_7.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_7.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_7.setObjectName(_fromUtf8("label_7"))
        self.horizontalLayout_4.addWidget(self.label_7)
        self.leNomBd = QtGui.QLineEdit(self.groupBox)
        self.leNomBd.setMinimumSize(QtCore.QSize(249, 0))
        self.leNomBd.setObjectName(_fromUtf8("leNomBd"))
        self.horizontalLayout_4.addWidget(self.leNomBd)
        self.formLayout.setLayout(2, QtGui.QFormLayout.LabelRole, self.horizontalLayout_4)
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setContentsMargins(63, -1, -1, -1)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.label_8 = QtGui.QLabel(self.groupBox)
        self.label_8.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_8.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_8.setObjectName(_fromUtf8("label_8"))
        self.horizontalLayout_5.addWidget(self.label_8)
        self.leSchema = QtGui.QLineEdit(self.groupBox)
        self.leSchema.setMinimumSize(QtCore.QSize(167, 0))
        self.leSchema.setObjectName(_fromUtf8("leSchema"))
        self.horizontalLayout_5.addWidget(self.leSchema)
        self.formLayout.setLayout(3, QtGui.QFormLayout.LabelRole, self.horizontalLayout_5)
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setContentsMargins(52, -1, -1, -1)
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.label_9 = QtGui.QLabel(self.groupBox)
        self.label_9.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_9.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_9.setObjectName(_fromUtf8("label_9"))
        self.horizontalLayout_6.addWidget(self.label_9)
        self.leUser = QtGui.QLineEdit(self.groupBox)
        self.leUser.setMinimumSize(QtCore.QSize(167, 0))
        self.leUser.setObjectName(_fromUtf8("leUser"))
        self.horizontalLayout_6.addWidget(self.leUser)
        self.formLayout.setLayout(4, QtGui.QFormLayout.LabelRole, self.horizontalLayout_6)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setContentsMargins(36, -1, -1, -1)
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.label_15 = QtGui.QLabel(self.groupBox)
        self.label_15.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_15.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_15.setObjectName(_fromUtf8("label_15"))
        self.horizontalLayout_12.addWidget(self.label_15)
        self.lePwd = QtGui.QLineEdit(self.groupBox)
        self.lePwd.setMinimumSize(QtCore.QSize(167, 0))
        self.lePwd.setObjectName(_fromUtf8("lePwd"))
        self.horizontalLayout_12.addWidget(self.lePwd)
        self.formLayout.setLayout(5, QtGui.QFormLayout.LabelRole, self.horizontalLayout_12)
        self.verticalLayout.addWidget(self.groupBox)
        self.btnBox = QtGui.QDialogButtonBox(configuration_form)
        self.btnBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.btnBox.setCenterButtons(True)
        self.btnBox.setObjectName(_fromUtf8("btnBox"))
        self.verticalLayout.addWidget(self.btnBox)

        self.retranslateUi(configuration_form)
        QtCore.QMetaObject.connectSlotsByName(configuration_form)

    def retranslateUi(self, configuration_form):
        configuration_form.setWindowTitle(_translate("configuration_form", "Geolimi - Configuration", None))
        self.groupBox.setTitle(_translate("configuration_form", "Paramètres de connexion  à la base de données", None))
        self.label_5.setText(_translate("configuration_form", "Hôte", None))
        self.label_6.setText(_translate("configuration_form", "Port", None))
        self.label_7.setText(_translate("configuration_form", "Nom de la BD", None))
        self.label_8.setText(_translate("configuration_form", "Schéma", None))
        self.label_9.setText(_translate("configuration_form", "Utilisateur", None))
        self.label_15.setText(_translate("configuration_form", "Mot de passe", None))

