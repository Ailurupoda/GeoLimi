# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Fenetre de gestion des districts
import sys
import os

# ERREUR LIGNE 51

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.districts_form import *
from forms.districts_ajout_form import *

class DistrictsAjoutDialog(QDialog, Ui_district_ajout_form):
    #Fenetre d'ajout d'un district
    def __init__(self, db, dbSchema,parent=None):
        super(DistrictsAjoutDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        #Insertion du district dans la base
        wdistr_distr = self.le_district.text()
        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".district_capture"
        query.prepare("INSERT INTO " + wrelation + " (distr_nom) VALUES (?)")
        query.addBindValue(wdistr_distr)
        if not query.exec_():
            QMessageBox.critical(self, u"Erreur - Création district", query.lastError().text(), QMessageBox.Ok)
        else:
            QDialog.accept(self)

class DistDialog(QDialog, Ui_districts_form):
    #Fenetre de gestion des districts
    def __init__(self, db, dbSchema, parent=None):
        super(DistDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)

        self.modelDistrict = QSqlTableModel(self, self.db)
        wrelation = self.dbSchema + ".district_capture"
        self.modelDistrict.setTable(wrelation)

        self.modelDistrict.setHeaderData(self.modelDistrict.fieldIndex("distr_id"), Qt.Horizontal, u"ID")
        self.modelDistrict.setHeaderData(self.modelDistrict.fieldIndex("distr_nom"), Qt.Horizontal, u"District capture")

        if (not self.modelDistrict.select()):
            QMessageBox.critical(self, u"Remplissage du modele", self.modelDistrict.lastError().text(), QMessageBox.Ok)
        self.modelDistrict.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.tvdistricts.setModel(self.modelDistrict)
        self.tvdistricts.setItemDelegate(DistrictsDelegate(self))
        self.tvdistricts.setSelectionMode(QTableView.SingleSelection)
        self.tvdistricts.setSelectionBehavior(QTableView.SelectRows)
        self.tvdistricts.setColumnHidden(self.modelDistrict.fieldIndex("distr_id"), True)
        self.tvdistricts.horizontalHeader().setStretchLastSection(True)

        self.connect(self.btnAdd, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.btnDelete, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def addRecord(self):
        #Ajout d'un enregistrement
        dialog = DistrictsAjoutDialog(self.db, self.dbSchema)
        dialog.setWindowModality(Qt.ApplicationModal)
        if dialog.exec_():
            self.modelDistrict.setFilter("")

    def deleteRecord(self):
        #Suppresion d'un enregistrement
        index = self.tvdistricts.currentIndex()
        if not index.isValid():
            return
        record = self.modelDistrict.record(index.row())
        wdistr_id = record.value(self.modelDistrict.fieldIndex("distr_id"))

        individusrecords = 0
        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".individu"
        query.prepare("SELECT COUNT(*) FROM " + wrelation + " WHERE ind_distr_id = ?")
        query.addBindValue(wdistr_id)

        if query.exec_():
            if query.next():
                individusrecords = query.value(0)

        if individusrecords > 0:
            QMessageBox.warning(self, u"Suppression",
                                    u"Ce district ne peut pas être supprimé car il est présent dans %i individu(s)" % individusrecords,
                                    QMessageBox.Ok)
        else:
            self.modelDistrict.removeRow(index.row())
            self.modelDistrict.submitAll()

    def reject(self):
        self.accept()

    def accept(self):
        QDialog.accept(self)


class DistrictsDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(DistrictsDelegate, self).__init__(parent)

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