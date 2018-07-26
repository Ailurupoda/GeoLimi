# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Fenêtre des types d'activité des oiseaux (fonction des marées)
import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.type_activite_form import *
from forms.type_activite_ajout import *


class ActiviteAjoutDialog(QDialog, Ui_type_activite_ajout_form):
    #Classe de lancement de la fenêtre d'ajout d'activité
    def __init__(self, db, dbSchema, parent=None):
        super(ActiviteAjoutDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        wtype_activite_nom = self.le_type_activite.text()

        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".type_activite"
        query.prepare("INSERT INTO " + wrelation + " (type_act_nom) VALUES (?)")
        query.addBindValue(wtype_activite_nom)

        if not query.exec_():
            QMessageBox.critical(self, u"Erreur - Création activité", query.lastError().text(), QMessageBox.Ok)
        else:
            QDialog.accept(self)


class TypeActiviteDialog(QDialog, Ui_type_activite_form):
    #Classe de lancement de la fenêtre des différents type d'activités
    def __init__(self, db, dbSchema, parent=None):
        #Initialisation des champs de la fenêtre
        super(TypeActiviteDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)

        #Récupération du model de la base
        self.modelTypeActivite = QSqlTableModel(self, self.db)
        wrelation = self.dbSchema + ".type_activite"
        self.modelTypeActivite.setTable(wrelation)

        self.modelTypeActivite.setHeaderData(self.modelTypeActivite.fieldIndex("type_act_id"), Qt.Horizontal, u"ID")
        self.modelTypeActivite.setHeaderData(self.modelTypeActivite.fieldIndex("type_act_nom"), Qt.Horizontal, u"Type d'activités")


        if (not self.modelTypeActivite.select()):
            QMessageBox.critical(self, u"Remplissage du modèle", self.model.lastError().text(), QMessageBox.Ok)
        self.modelTypeActivite.setEditStrategy(QSqlTableModel.OnFieldChange)
        #Calque de la table view sur le model de la base
        self.tvType_activite.setModel(self.modelTypeActivite)
        self.tvType_activite.setItemDelegate(ActiviteDelegate(self))
        self.tvType_activite.setSelectionMode(QTableView.SingleSelection)
        self.tvType_activite.setSelectionBehavior(QTableView.SelectRows)
        self.tvType_activite.setColumnHidden(self.modelTypeActivite.fieldIndex("type_act_id"), True)
        self.tvType_activite.horizontalHeader().setStretchLastSection(True)

        self.connect(self.btnAdd, SIGNAL("clicked()"), self.addRecord)
        self.connect(self.btnDelete, SIGNAL("clicked()"), self.deleteRecord)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def addRecord(self):
        #Fonction d'ajout d'un enregistrement (appel à la classe en haut)
        dialog = ActiviteAjoutDialog(self.db, self.dbSchema)
        dialog.setWindowModality(Qt.ApplicationModal)
        if dialog.exec_():
            self.modelTypeActivite.setFilter("")

    def deleteRecord(self):
        #Fonction de suppression d'enregistrement
        #Vérifie le lien avec les autres données
        index = self.tvType_activite.currentIndex()
        if not index.isValid():
            return
        record = self.modelTypeActivite.record(index.row())
        wtype_act_id = record.value(self.modelTypeActivite.fieldIndex("type_act_id"))

        activiterecords = 0
        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".observation"
        query.prepare("SELECT COUNT(*) FROM " + wrelation + " WHERE obs_type_act_id = ? ")
        # query.prepare("SELECT COUNT(*) FROM " + wrelation + " WHERE obs_type_act_id = ?")
        query.addBindValue(wtype_act_id)

        if query.exec_():
            if query.next():
                activiterecords = query.value(0)

        if activiterecords > 0:
            QMessageBox.warning(self, u"Suppression",
                                u"Cette activité ne peut pas être supprimée car elle est présente dans %i observation(s)" % activiterecords,
                                QMessageBox.Ok)
        else:
            self.modelTypeActivite.removeRow(index.row())
            self.modelTypeActivite.submitAll()

    def reject(self):
        self.accept()

    def accept(self):
        QDialog.accept(self)


class ActiviteDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(ActiviteDelegate, self).__init__(parent)

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

