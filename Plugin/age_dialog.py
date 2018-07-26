# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Fenêtre de gestion des ages
import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.age_form import *
from forms.age_ajout_form import *

class AgeAjoutDialog(QDialog, Ui_age_ajout_form):
    #Classeouvrant la fenêtre d'ajout d'un age
    def __init__(self, db, dbSchema,parent=None):
        #Initialisation de la fenêtre
        #Récupération des informations de la base
        super(AgeAjoutDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

    def reject(self):
        #Annulation
        QDialog.reject(self)

    def accept(self):
        #Confirmation et insertion dans la base en cliquant sur Ok
        wage_age = self.le_age.text()
        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".age"
        query.prepare("INSERT INTO " + wrelation + " (age_libelle) VALUES (?)")
        query.addBindValue(wage_age)
        if not query.exec_():
            QMessageBox.critical(self, u"Erreur - Création age", query.lastError().text(), QMessageBox.Ok)
        else:
            QDialog.accept(self)

class AgeDialog(QDialog, Ui_age_form):
    #Classe ouvrant la fenêtre de gestion des âges
    def __init__(self, db, dbSchema, parent=None):
        #Initialisation des informations contenues par la fenêtre
        super(AgeDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)

        #Connexion des données de la base
        self.modelAge = QSqlTableModel(self, self.db)
        wrelation = self.dbSchema + ".age"
        self.modelAge.setTable(wrelation)
        #Récupération des informations d'age selon l'id et le champ Age
        self.modelAge.setHeaderData(self.modelAge.fieldIndex("age_id"), Qt.Horizontal, u"ID")
        self.modelAge.setHeaderData(self.modelAge.fieldIndex("age_libelle"), Qt.Horizontal, u"Age")

        if (not self.modelAge.select()):
            QMessageBox.critical(self, u"Remplissage du modèle", self.model.lastError().text(), QMessageBox.Ok)
        self.modelAge.setEditStrategy(QSqlTableModel.OnFieldChange)
        #Association du modèle la table view
        self.tvage.setModel(self.modelAge)
        self.tvage.setItemDelegate(AgeDelegate(self))
        self.tvage.setSelectionMode(QTableView.SingleSelection)
        self.tvage.setSelectionBehavior(QTableView.SelectRows)
        self.tvage.setColumnHidden(self.modelAge.fieldIndex("age_id"), True)
        self.tvage.horizontalHeader().setStretchLastSection(True)

        #Initialisation des actions sur les boutons
        self.connect(self.btnAdd, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.btnDelete, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def addRecord(self):
        #Ajout d'un nouvel enregistrement
        #Utilisation de la classe d'ajout (plus haut)
        dialog = AgeAjoutDialog(self.db, self.dbSchema)
        dialog.setWindowModality(Qt.ApplicationModal)
        if dialog.exec_():
            self.modelAge.setFilter("")

    def deleteRecord(self):
        #Suppression d'un enregistrement
        index = self.tvage.currentIndex()
        if not index.isValid():
            return
        record = self.modelAge.record(index.row())
        wesp_id = record.value(self.modelAge.fieldIndex("age_id"))

        individusrecords = 0
        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".individu"
        query.prepare("SELECT COUNT(*) FROM " + wrelation + " WHERE ind_age_id = ?")
        query.addBindValue(wesp_id)

        if query.exec_():
            if query.next():
                individusrecords = query.value(0)

        if individusrecords > 0:
            #Test de la présence d'information contenu pour l'age précisé
            QMessageBox.warning(self, u"Suppression",
                                u"Cet age ne peut pas être supprimé car il est présent dans %i individu(s)" % individusrecords,
                                QMessageBox.Ok)
        else:
            #Suppression total de la ligne
            self.modelAge.removeRow(index.row())
            self.modelAge.submitAll()

    def reject(self):
        #Quitter la fenêtre
        self.accept()

    def accept(self):
        #Quitter la fenêtre
        QDialog.accept(self)


class AgeDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(AgeDelegate, self).__init__(parent)

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