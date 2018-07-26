# -*- coding: utf-8 -*-

#Antoine Blain, COrentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Import de données Lune
import sys
import os
import time
import psycopg2
import shutil
import pickle

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.import_lune_form import *

class ImportLuneDialog(QDialog, Ui_import_lune_form):
    #Classe récupérant les informations de la fenêtre
    def __init__(self, parent = None):
        #Initialisation de la fenêtre d'import Lune
        super(ImportLuneDialog, self).__init__(parent)

        self.setupUi(self)

        self.lune_a_inserer = ""

        #Initialisation des connexions des effets de l'interaction sur les boutons
        self.connect(self.btnSelectionFichier, SIGNAL("clicked()"), self.selectionFichier)
        self.connect(self.btnLancementEtape1, SIGNAL("clicked()"), self.lancementEtape1)
        self.connect(self.btnLancementEtape2, SIGNAL("clicked()"), self.lancementEtape2)
        self.connect(self.btnLancementEtape3, SIGNAL("clicked()"), self.lancementEtape3)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def selectionFichier(self):
        #Fonction sélectionnant le fichier à importer
        #Ouvre une fenetre demandant de rechercher le fichier à importer
        #Débloque l'accès à l'étape suivante
        self.btnLancementEtape1.setEnabled(False)
        self.btnLancementEtape2.setEnabled(False)
        self.btnLancementEtape3.setEnabled(False)
        fichier = QFileDialog.getOpenFileName(self, u"Ouvrir un fichier", u"D:\PTUT", "Lune(*.csv)")
        if fichier:
            self.lbl_url_fichier.setText(fichier)#Récupération et affichage du chemin du fichier
            self.btnLancementEtape1.setEnabled(True)

    def lancementEtape1(self):
        #Fonction de lancement de l'étape 1
        #Parcours les données du fichier en enlevant l'en tête et les lignes vides
        #Affiche le nombre d'information devant être parcourues.
        self.btnLancementEtape2.setEnabled(False)
        self.btnLancementEtape3.setEnabled(False)
        fichier_lune = open(self.lbl_url_fichier.text(), "rb")
        contenu = fichier_lune.read()
        contenu = contenu.split('\n')
        listRemov = [contenu[0]]
        col = contenu[0].split(';')

        cptPb = 1.0
        incPb = 100.0 / float(len(contenu))

        for row in contenu:
            self.pbEtape1.setValue(cptPb)
            if ';' not in row:
                listRemov.append(row)
            else:
                cptPb += incPb
        for rem in listRemov:
            contenu.remove(rem)

        msg = u"Le fichier sélectionné contient %i colonnes et %i lignes à insérer." % (len(col), len(contenu))   #Indique le contenu et le col définit avant
        QMessageBox.information(QWidget(), u"Informations sur le contenu du fichier", msg)
        fichier_lune.close()
        self.btnLancementEtape2.setEnabled(True)#Active l'accès à l'étape suivant
        self.lune_a_inserer = contenu #Mise à jour des données à parcourir.

    def lancementEtape2(self):
        #Fonction de lancement de l'étape 2
        #Parcours les données à la recherche de lignes sans information qui ne seront alors pas insérées
        self.btnLancementEtape3.setEnabled(False)
        contenu = self.lune_a_inserer
        ligneVide = []

        cptVide = 0  # Nb ligne avec des informations manquante
        cptInfo = 0  # Nb ligne sans information

        cptPb = 1.0    #PROGRESS BARR
        incPb = 100.0/float(len(contenu))  #PROGRESS BARR


        db, dbSchema = self.connexion()

        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...", QMessageBox.Ok)
        else:
            i = 0
            while i < (len(contenu)):
                #Parcours du contenu en enlevant les données qui ne nous intéressent pas
                self.pbEtape2.setValue(cptPb)
                rowTmp = contenu[i].split(';')
                if len(rowTmp[3]) == 0  :
                    cptVide =+ 1
                    ligneVide.append(rowTmp)
                    contenu.remove(contenu[i])
                elif len(rowTmp[4]) == 0 :
                    cptInfo = + 1
                    ligneVide.append(rowTmp)
                    contenu.remove(contenu[i])
                else :
                    i += 1
                    cptPb += incPb

            msg = u"Le fichier contient %i lignes erronées :\n" % (cptVide  + cptInfo)
            msg += u"   - Il y a %i lignes sans date\n" % (cptVide)
            msg += u"   - Il y a %i lignes sans phase\n" % (cptInfo)
            msg += u"Il reste %i lignes à insérer\n" % (len(contenu))
            QMessageBox.information(QWidget(), u"Informations sur le contenu du fichier", msg)

            self.date_a_inserer = contenu#Récupération du contenu mis à jour
            if len(contenu) > 0:
                self.btnLancementEtape3.setEnabled(True)#Accès à l'étape 3 si il y a des lignes à insérer


    def lancementEtape3(self):
        #Fonction de lancement de l'étape 3
        #Parcours les données restantes et insertion dans la base de données
        if len(self.date_a_inserer) > 0:
            #Connexion à la base
            db, dbSchema = self.connexion()

            if (not db.open()):
                QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",  QMessageBox.Ok)
            else:
            #Lorsque la connexion est bien effectuée, on va parcourir le fichier
                contenu = self.date_a_inserer
                cptPb = 1.0
                incPb = 100.0 / float(len(contenu))
                nbRowInser = 0
                nbRowExist = 0
                for row in contenu:
                    self.pbEtape3.setValue(cptPb)
                    row = row.split(';')
                    date = row[3]
                    if len(row[4]) > 0:
                        phase = row[4].replace(",", ".")
                    else:
                        phase = None

                    #Préparation de la requête d'insertion
                    queryInsLune = QSqlQuery(db)
                    wrelation = dbSchema + ".lune"
                    queryInsLune.prepare("INSERT INTO brut.lune (lune_date, lune_phase) VALUES (?, ?)")
                    queryInsLune.addBindValue(date)#Ajout de la date à insérer
                    queryInsLune.addBindValue(phase)#Ajout de la phase à insérer

                    if not queryInsLune.exec_():
                        if u"la valeur d'une clé dupliquée rompt la contrainte unique « uq_lune »" in queryInsLune.lastError().text():
                            nbRowExist += 1
                            #Insertion de données déjà présente = renvoie d'une erreur SQL, on n'affiche pas le message alors.
                        else:
                            QMessageBox.critical(self, u"Erreur - Insertion Lune", queryInsLune.lastError().text(), QMessageBox.Ok)
                    else:
                        nbRowInser += 1
                    cptPb += incPb
                QMessageBox.information(self, u'Information - Insertion Lune',u"%i lignes ont été  intégrées\n %i lignes étaient déjà présentes." % (nbRowInser, nbRowExist))


    def connexion(self):
        #Fonction de connexion à la base de données
        s = QSettings()

        hote = s.value("geolimi/config/hote", "localhost")
        port = s.value("geolimi/config/port", "5432")
        dbname = s.value("geolimi/config/nomBd", "GeoLimi")
        schema = s.value("geolimi/config/schema", "brut")
        user = s.value("geolimi/config/user", "postgres")
        pwd = s.value("geolimi/config/pwd", "pgAdmin")

        db = QSqlDatabase.addDatabase("QPSQL", "db1")
        db.setHostName(hote)
        db.setPort(int(port))
        db.setDatabaseName(dbname)
        dbSchema = schema
        db.setUserName(user)
        db.setPassword(pwd)
        return db, dbSchema

    def reject(self):
        self.accept()

    def accept(self):
        QDialog.accept(self)
