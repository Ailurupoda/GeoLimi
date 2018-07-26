# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Fenetre listant les informations sur les fichiers
import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.visualiseur_fichier_form import *
from forms.import_observation_form import*


class FichierDialog(QDialog, Ui_fichier_visualiseur_form):
    #Classe de lancement de la fenêtre de visualisation des différents fichiers insérés
    def __init__(self, db, dbSchema, parent=None):
        #Initialisation des champs de la fenêtre
        super(FichierDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)

        #Création du calque de la table fichier de la base
        self.modelFichier = QSqlTableModel(self, self.db)
        wrelation = self.dbSchema + ".fichier"
        self.modelFichier.setTable(wrelation)

        self.modelFichier.setHeaderData(self.modelFichier.fieldIndex("fich_id"), Qt.Horizontal, u"ID")
        self.modelFichier.setHeaderData(self.modelFichier.fieldIndex("fich_date_insert"), Qt.Horizontal, u"Date d'insertion")
        self.modelFichier.setHeaderData(self.modelFichier.fieldIndex("fich_chemin"), Qt.Horizontal, u"Chemin du fichier")

        if (not self.modelFichier.select()):
            QMessageBox.critical(self, u"Remplissage du modèle", self.model.lastError().text(), QMessageBox.Ok)
        self.modelFichier.setEditStrategy(QSqlTableModel.OnFieldChange)
        #Affichage des données du calque sur la table view
        self.tv_visualiseur_fichier.setModel(self.modelFichier)
        self.tv_visualiseur_fichier.setItemDelegate(FichierDelegate(self))
        self.tv_visualiseur_fichier.setSelectionMode(QTableView.SingleSelection)
        self.tv_visualiseur_fichier.setSelectionBehavior(QTableView.SelectRows)
        self.tv_visualiseur_fichier.setColumnHidden(self.modelFichier.fieldIndex("fich_id"), True)
        self.tv_visualiseur_fichier.setColumnHidden(self.modelFichier.fieldIndex("fich_goel_id"), True)
        self.tv_visualiseur_fichier.horizontalHeader().setStretchLastSection(True)

        self.connect(self.btnAdd, SIGNAL("clicked()"), self.addFichier)
        self.connect(self.btnDelete, SIGNAL("clicked()"), self.deleteFichier)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def addFichier(self):
        #Ajout d'un enregistrement
        dialog = ImportObservationDialog(self)
        dialog.setWindowModality(Qt.ApplicationModal)
        if dialog.exec_():
            self.modelFichier.setFilter("")

    def deleteFichier(self):
        #Suppression d'un enregistrement
        #Vérification de non utilisation
        index = self.tv_visualiseur_fichier.currentIndex()
        if not index.isValid():
            return
        record = self.modelFichier.record(index.row())
        wfich_id = record.value(self.modelFichier.fieldIndex("fich_id"))

        individusrecords = 0
        query = QSqlQuery(self.db)

        wrelation = self.dbSchema + ".observation"
        query.prepare("SELECT COUNT(*) FROM " + wrelation + " WHERE obs_fich_id = ?")
        query.addBindValue(wfich_id)

        if query.exec_():
            if query.next():
                individusrecords = query.value(0)

        if individusrecords > 0:
            QMessageBox.warning(self, u"Suppression",
                                u"Ce fichier ne peut pas être supprimé car il concerne %i individu(s)" % individusrecords,
                                QMessageBox.Ok)
        else:
            self.modelFichier.removeRow(index.row())
            self.modelFichier.submitAll()

    def reject(self):
        self.accept()

    def accept(self):
        QDialog.accept(self)


class FichierDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(FichierDelegate, self).__init__(parent)

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

