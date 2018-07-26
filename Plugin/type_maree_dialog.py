# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Fenêtre des types de marées
import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.type_maree_form import *
from forms.type_maree_ajout import *


class MareeAjoutDialog(QDialog, Ui_type_maree_ajout):
    #Classe de lancement de la fenêtre d'ajout d'un type de arée
    def __init__(self, db, dbSchema, parent=None):
        #Initialisation des champs de la fenêtre
        super(MareeAjoutDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        wtype_maree = self.le_type_maree.text()

        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".type_maree"
        query.prepare("INSERT INTO " + wrelation + " (tymar_libelle) VALUES (?)")
        query.addBindValue(wtype_maree)

        if not query.exec_():
            QMessageBox.critical(self, u"Erreur - Création d'un type marée", query.lastError().text(), QMessageBox.Ok)
        else:
            QDialog.accept(self)


class MareeDialog(QDialog, Ui_type_maree_form):
    #CLasse de lancement de la fenêtre de gestion des types de marée
    def __init__(self, db, dbSchema, parent=None):
        #Initialisation des champs de la fenêtre
        super(MareeDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)
        #Création d'un calque de la table de la base
        self.modelMaree = QSqlTableModel(self, self.db)
        wrelation = self.dbSchema + ".type_maree"
        self.modelMaree.setTable(wrelation)

        self.modelMaree.setHeaderData(self.modelMaree.fieldIndex("tymar_id"), Qt.Horizontal, u"ID")
        self.modelMaree.setHeaderData(self.modelMaree.fieldIndex("tymar_libelle"), Qt.Horizontal, u"Type de marée")
        # self.modelMaree.setHeaderData(self.modelMaree.fieldIndex("esp_nom_latin"), Qt.Horizontal, u"Nom latin")

        if (not self.modelMaree.select()):
            QMessageBox.critical(self, u"Remplissage du modèle", self.model.lastError().text(), QMessageBox.Ok)
        self.modelMaree.setEditStrategy(QSqlTableModel.OnFieldChange)
        #Utilisation du calque de la table pour afficher les données dans la table view
        self.tvType_maree.setModel(self.modelMaree)
        self.tvType_maree.setItemDelegate(MareeDelegate(self))
        self.tvType_maree.setSelectionMode(QTableView.SingleSelection)
        self.tvType_maree.setSelectionBehavior(QTableView.SelectRows)
        self.tvType_maree.setColumnHidden(self.modelMaree.fieldIndex("tymar_id"), True)
        self.tvType_maree.horizontalHeader().setStretchLastSection(True)

        self.connect(self.btnAdd, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.btnDelete, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def addRecord(self):
        #Fonction d'ajout d'un enregistrement ( lancement de la classe en haut)
        dialog = MareeAjoutDialog(self.db, self.dbSchema)
        dialog.setWindowModality(Qt.ApplicationModal)
        if dialog.exec_():
            self.modelMaree.setFilter("")

    def deleteRecord(self):
        #Fonction de suppression d'un enregistrement
        index = self.tvType_maree.currentIndex()
        if not index.isValid():
            return
        record = self.modelMaree.record(index.row())
        wmaree_id = record.value(self.modelMaree.fieldIndex("tymar_id"))

        mareerecords = 0
        query = QSqlQuery(self.db)

        # a_type_maree deviendra "periode"
        wrelation = self.dbSchema + ".a_type_maree"
        query.prepare("SELECT COUNT(*) FROM " + wrelation + " WHERE atm_tymar_id = ?")
        query.addBindValue(wmaree_id)

        if query.exec_():
            if query.next():
                mareerecords = query.value(0)

        if mareerecords > 0:
            QMessageBox.warning(self, u"Suppression",
                                u"Ce type de marée ne peut pas être supprimé car il est présent dans %i individu(s)" % mareerecords,
                                QMessageBox.Ok)
        else:
            self.modelMaree.removeRow(index.row())
            self.modelMaree.submitAll()

    def reject(self):
        self.accept()

    def accept(self):
        QDialog.accept(self)


class MareeDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(MareeDelegate, self).__init__(parent)

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

