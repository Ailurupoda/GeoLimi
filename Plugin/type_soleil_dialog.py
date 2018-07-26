# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Fenetre listant les types de soleil
import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.type_soleil_form import *
from forms.type_soleil_ajout import *


class SoleilAjoutDialog(QDialog, Ui_type_soleil_ajout):
    def __init__(self, db, dbSchema, parent=None):
        super(SoleilAjoutDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        wtype_soleil = self.le_type_soleil.text()

        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".type_soleil"
        query.prepare("INSERT INTO " + wrelation + " (type_sol_libelle) VALUES (?)")
        query.addBindValue(wtype_soleil)


        if not query.exec_():
            QMessageBox.critical(self, u"Erreur - Création d'un type soleil", query.lastError().text(), QMessageBox.Ok)
        else:
            QDialog.accept(self)


class SoleilDialog(QDialog, Ui_type_soleil_form):
    def __init__(self, db, dbSchema, parent=None):
        super(SoleilDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)

        self.modelSoleil = QSqlTableModel(self, self.db)
        wrelation = self.dbSchema + ".type_soleil"
        self.modelSoleil.setTable(wrelation)

        self.modelSoleil.setHeaderData(self.modelSoleil.fieldIndex("type_sol_id"), Qt.Horizontal, u"ID")
        self.modelSoleil.setHeaderData(self.modelSoleil.fieldIndex("type_sol_libelle"), Qt.Horizontal, u"État de la journée")

        if (not self.modelSoleil.select()):
            QMessageBox.critical(self, u"Remplissage du modèle", self.model.lastError().text(), QMessageBox.Ok)
        self.modelSoleil.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.tvType_soleil.setModel(self.modelSoleil)
        self.tvType_soleil.setItemDelegate(SoleilDelegate(self))
        self.tvType_soleil.setSelectionMode(QTableView.SingleSelection)
        self.tvType_soleil.setSelectionBehavior(QTableView.SelectRows)
        self.tvType_soleil.setColumnHidden(self.modelSoleil.fieldIndex("type_sol_id"), True)
        self.tvType_soleil.horizontalHeader().setStretchLastSection(True)

        self.connect(self.btnAdd, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.btnDelete, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def addRecord(self):
        dialog = SoleilAjoutDialog(self.db, self.dbSchema)
        dialog.setWindowModality(Qt.ApplicationModal)
        if dialog.exec_():
            self.modelSoleil.setFilter("")

    def deleteRecord(self):
        index = self.tvType_soleil.currentIndex()
        if not index.isValid():
            return
        record = self.modelSoleil.record(index.row())
        wtype_sol_id = record.value(self.modelSoleil.fieldIndex("type_sol_id"))

        soleilrecords = 0
        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".soleil"
        query.prepare("SELECT COUNT(*) FROM " + wrelation + " WHERE sol_type_sol_id = ?")
        query.addBindValue(wtype_sol_id)

        if query.exec_():
            if query.next():
                soleilrecords = query.value(0)

        if soleilrecords > 0:
            QMessageBox.warning(self, u"Suppression",
                                u"Cet état de la journée ne peut pas être supprimé car il est présent dans %i individu(s)" % soleilrecords,
                                QMessageBox.Ok)
        else:
            self.modelSoleil.removeRow(index.row())
            self.modelSoleil.submitAll()

    def reject(self):
        self.accept()

    def accept(self):
        QDialog.accept(self)


class SoleilDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(SoleilDelegate, self).__init__(parent)

    def paint(self, painter, option, index):
        myoption = QStyleOptionViewItem(option)
        # if index.column() == ROOM:
        #    myoption.displayAlignment |= Qt.AlignRight|Qt.AlignVCenter
        QSqlRelationalDelegate.paint(self, painter, myoption, index)

    def createEditor(self, parent, option, index):
        '''
        if index.column() == ROOM:
            editor = QLineEdit(parent)
            regex = QRegExp(r"(?:0[1-9]|1[0124-9]|2[0-7])"
                            r"(?:0[1-9]|[1-5][0-9]|6[012])")
            validator = QRegExpValidator(regex, parent)
            editor.setValidator(validator)
            editor.setInputMask("9999")
            editor.setAlignment(Qt.AlignRight|Qt.AlignVCenter)
            return editor
        else:
            return QSqlRelationalDelegate.createEditor(self, parent, option, index)
        '''
        return QSqlRelationalDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        '''
        if index.column() == ROOM:
            text = index.model().data(index, Qt.DisplayRole).toString()
            editor.setText(text)
        else:
            QSqlRelationalDelegate.setEditorData(self, editor, index)
        '''
        QSqlRelationalDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        '''
        if index.column() == ROOM:
            model.setData(index, QVariant(editor.text()))
        else:
            QSqlRelationalDelegate.setModelData(self, editor, model, index)
        '''
        QSqlRelationalDelegate.setModelData(self, editor, model, index)

