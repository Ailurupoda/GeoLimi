# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Gestion des cycles biologiques
import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.cycle_bio_ajout_form import *
from forms.cycle_bio_form import *

class CycleAjoutDialog(QDialog, Ui_cycle_bio_ajout):
    #Classe de lancement de la fenêtre d'ajout de cycle
    def __init__(self, db, dbSchema,parent=None):
        super(CycleAjoutDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        #Insertion du cycle dans la base
        wesp_cyclebio = self.le_cycle_bio.text()
        print(wesp_cyclebio)
        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".cycle_biologique"
        query.prepare("INSERT INTO " + wrelation + "(cycle_libelle) VALUES (?)")
        query.addBindValue(wesp_cyclebio)

        if not query.exec_():
            QMessageBox.critical(self, u"Erreur - Création cylcle biologique", query.lastError().text(), QMessageBox.Ok)
        else:
            QDialog.accept(self)

class CycleDialog(QDialog, Ui_cycle_bio):
    #Classe de lancement de la fenêtre de gestion des cycles
    def __init__(self, db, dbSchema, parent=None):
        #Initialisation des champs de la fenêtre
        super(CycleDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)

        self.modelCycle = QSqlTableModel(self, self.db)
        wrelation = self.dbSchema + ".cycle_biologique"
        self.modelCycle.setTable(wrelation)

        self.modelCycle.setHeaderData(self.modelCycle.fieldIndex("cycle_id"), Qt.Horizontal, u"ID")
        self.modelCycle.setHeaderData(self.modelCycle.fieldIndex("cycle_libelle"), Qt.Horizontal, u"libelle du cycle biologique")

        if (not self.modelCycle.select()):
            QMessageBox.critical(self, u"Remplissage du modèle", self.model.lastError().text(), QMessageBox.Ok)
        self.modelCycle.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.tvcycle_bio.setModel(self.modelCycle)
        self.tvcycle_bio.setItemDelegate(CycleDelegate(self))
        self.tvcycle_bio.setSelectionMode(QTableView.SingleSelection)
        self.tvcycle_bio.setSelectionBehavior(QTableView.SelectRows)
        self.tvcycle_bio.setColumnHidden(self.modelCycle.fieldIndex("cycle_id"), True)
        self.tvcycle_bio.horizontalHeader().setStretchLastSection(True)

        self.connect(self.btnAdd, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.btnDelete, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def addRecord(self):
        #Ajout d'un enregistrement
        dialog = CycleAjoutDialog(self.db, self.dbSchema)
        dialog.setWindowModality(Qt.ApplicationModal)
        if dialog.exec_():
            self.modelCycle.setFilter("")

    def deleteRecord(self):
        #Suppression d'un enregistrement
        index = self.tvcycle_bio.currentIndex()
        if not index.isValid():
            return
        record = self.modelCycle.record(index.row())
        wesp_id = record.value(self.modelCycle.fieldIndex("obs_id"))

        observationrecords = 0
        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".observation"
        query.prepare("SELECT COUNT(*) FROM " + wrelation + " WHERE obs_cycle_id = ?")
        query.addBindValue(wesp_id)

        if query.exec_():
            if query.next():
                observationrecords = query.value(0)

        if observationrecords > 0:
            QMessageBox.warning(self, u"Suppression",
                                u"Cette espèce ne peut pas être supprimée car elle est présente dans %i individu(s)" % individusrecords,
                                QMessageBox.Ok)
        else:
            self.modelCycle.removeRow(index.row())
            self.modelCycle.submitAll()

        def reject(self):
            self.accept()

        def accept(self):
            QDialog.accept(self)


class CycleDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(CycleDelegate, self).__init__(parent)

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
