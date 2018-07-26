# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Fenetre de gestion des espèces
import sys 
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.espece_form import *
from forms.espece_ajout_form import *

class EspeceAjoutDialog(QDialog, Ui_espece_ajout_form):
    #Fenetre d'ajout d'une espèce
    def __init__(self, db, dbSchema,parent=None):
        super(EspeceAjoutDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)
        
    def reject(self):
        QDialog.reject(self)

    def accept(self):
        #Insertion de l'espèce dans la base
        wesp_nomfr = self.le_esp_nomfr.text()
        wesp_nom_latin = self.le_esp_nom_latin.text()
        query = QSqlQuery(self.db)
        
        wrelation = self.dbSchema + ".espece"
        query.prepare("INSERT INTO " + wrelation + " (esp_nomfr, esp_nom_latin) VALUES (?, ?)")
        query.addBindValue(wesp_nomfr)
        query.addBindValue(wesp_nom_latin)
        if not query.exec_():
            QMessageBox.critical(self, u"Erreur - Création espèce", query.lastError().text(), QMessageBox.Ok)
        else:
            QDialog.accept(self)

class EspeceDialog(QDialog, Ui_espece_form):
    #Fenêtre de gestion des espèces
    def __init__(self, db, dbSchema, parent=None):
        super(EspeceDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)

        self.modelEspece = QSqlTableModel(self, self.db)
        wrelation = self.dbSchema + ".espece"
        self.modelEspece.setTable(wrelation)

        self.modelEspece.setHeaderData(self.modelEspece.fieldIndex("esp_id"), Qt.Horizontal, u"ID")
        self.modelEspece.setHeaderData(self.modelEspece.fieldIndex("esp_nomfr"), Qt.Horizontal, u"Nom français")
        self.modelEspece.setHeaderData(self.modelEspece.fieldIndex("esp_nom_latin"), Qt.Horizontal, u"Nom latin")

        if (not self.modelEspece.select()):
            QMessageBox.critical(self, u"Remplissage du modèle", self.model.lastError().text(), QMessageBox.Ok)
        self.modelEspece.setEditStrategy(QSqlTableModel.OnFieldChange)

        self.tvEspece.setModel(self.modelEspece)
        self.tvEspece.setItemDelegate(EspeceDelegate(self))
        self.tvEspece.setSelectionMode(QTableView.SingleSelection)
        self.tvEspece.setSelectionBehavior(QTableView.SelectRows)
        self.tvEspece.setColumnHidden(self.modelEspece.fieldIndex("esp_id"), True)
        self.tvEspece.horizontalHeader().setStretchLastSection(True)

        self.connect(self.btnAdd, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.btnDelete, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def addRecord(self):
        #Ajout d'une espèce
        dialog = EspeceAjoutDialog(self.db, self.dbSchema)
        dialog.setWindowModality(Qt.ApplicationModal)
        if dialog.exec_():
            self.modelEspece.setFilter("")

    def deleteRecord(self):
        #Suppresion d'une espèce
        index = self.tvEspece.currentIndex()
        if not index.isValid():
            return
        record = self.modelEspece.record(index.row())
        wesp_id = record.value(self.modelEspece.fieldIndex("esp_id"))
        
        individusrecords = 0
        query = QSqlQuery(self.db)
        
        wrelation = self.dbSchema + ".individu"
        query.prepare("SELECT COUNT(*) FROM " + wrelation + " WHERE ind_esp_id = ?")
        query.addBindValue(wesp_id)
        
        if query.exec_():
            if query.next():
                individusrecords = query.value(0)
        
        if individusrecords > 0:
            QMessageBox.warning(self, u"Suppression", u"Cette espèce ne peut pas être supprimée car elle est présente dans %i individu(s)" % individusrecords, QMessageBox.Ok)
        else:
            self.modelEspece.removeRow(index.row())
            self.modelEspece.submitAll()
        
    def reject(self):
        self.accept()

    def accept(self):
        QDialog.accept(self)
        
class EspeceDelegate(QSqlRelationalDelegate):

    def __init__(self, parent=None):
        super(EspeceDelegate, self).__init__(parent)


    def paint(self, painter, option, index):
        myoption = QStyleOptionViewItem(option)
        #if index.column() == ROOM:
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
            
            