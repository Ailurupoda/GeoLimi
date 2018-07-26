# -*- coding: utf-8 -*-

#Antoine Blain, COrentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Import données météos

import sys
import os
import time
import psycopg2
import shutil
import pickle

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.import_meteo_form import *

class ImportMeteoDialog(QDialog, Ui_import_meteo_form):
    def __init__(self, parent = None):
        super(ImportMeteoDialog, self).__init__(parent)
        # Initialisation de la fenêtre d'import

        self.setupUi(self)

        self.obs_a_inserer = []#Création de la liste de météos à insérer

        # Connexion des boutons à leurs effets
        self.connect(self.btnSelectionFichier, SIGNAL("clicked()"), self.selectionFichier)
        self.connect(self.btnLancementEtape1, SIGNAL("clicked()"), self.lancementEtape1)
        self.connect(self.btnLancementEtape2, SIGNAL("clicked()"), self.lancementEtape2)
        self.connect(self.btnLancementEtape3, SIGNAL("clicked()"), self.lancementEtape3)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def selectionFichier(self):
        # Fonction de sélection du fichier
        # Demande le chemin du fichier à parcourir
        # Active l'étape suivante
        self.pbEtape1.setValue(0)
        self.pbEtape2.setValue(0)
        self.pbEtape3.setValue(0)
        self.btnLancementEtape1.setEnabled(False)
        self.btnLancementEtape2.setEnabled(False)
        self.btnLancementEtape3.setEnabled(False)
        fichier = QFileDialog.getOpenFileName(self, u"Ouvrir un fichier", u"D:\PTUT", "Logger(*.csv)")
        if fichier:
            self.lbl_url_fichier.setText(fichier)
            self.btnLancementEtape1.setEnabled(True)

    def lancementEtape1(self):
        # Fonction de lancement de l'étape 1
        # Parcour le fichier et prend en compte les données hors entête et hors ligne vide
        # Informe sur le nombre de lignes à parcourir ainsi que le nombre de colonnes contenues
        self.pbEtape2.setValue(0)
        self.pbEtape3.setValue(0)
        self.btnLancementEtape2.setEnabled(False)
        self.btnLancementEtape3.setEnabled(False)
        fichier_obs = open(self.lbl_url_fichier.text(), "rb")
        contenu = fichier_obs.read()
        contenu = contenu.split('\n')
        listRemov = [contenu[0]]
        col = contenu[0].split(';')
        cptPb = 1.0
        incPb = 100.0/float(len(contenu) - 1)
        for row in contenu:
            self.pbEtape1.setValue(cptPb)
            if ';' not in row:
                listRemov.append(row)
            else:
                cptPb += incPb
        for rem in listRemov:
            contenu.remove(rem)

        msg = u"Le fichier sélectionné contient %i colonnes et %i lignes à insérer." % (len(col), len(contenu))
        QMessageBox.information(QWidget(), u"Informations sur le contenu du fichier", msg)
        fichier_obs.close()
        self.btnLancementEtape2.setEnabled(True)
        self.obs_a_inserer = contenu

    def lancementEtape2(self):
        # Fonction de lancement de l'étape 2
        # Parcours des données en enlevant les données non utilisables (trop d'infos manquantes)
        # Affiche le résultat du parcours
        self.pbEtape3.setValue(0)
        self.btnLancementEtape3.setEnabled(False)
        contenu = self.obs_a_inserer

        ligneVide = []
        ligneExist = []

        cptVide = 0#Nb ligne avec des informations manquante
        cptExist = 0#Nb lignes déjà présentes
        cptInfo = 0#Nb ligne sans information
        cptObs = 0#Nb ligne dont la date n'est pas concernée par une observation

        cptPb = 1.0
        incPb = 100.0 / float(len(contenu))

        listDate = [] #Liste des date dans la table météo
        listObs = [] #liste des date dans la table obs

        db, dbSchema = self.connexion()

        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...", QMessageBox.Ok)
        else:
            #Récupération des dates présentes dans la base concernant une météo
            wrelation = dbSchema + ".meteo"
            queryDate = QSqlQuery(db)
            queryDate.prepare("SELECT met_date, met_heure FROM " + wrelation)
            if queryDate.exec_():
                while queryDate.next():
                    listDate.append((queryDate.value(0), queryDate.value(1)))


            i = 0
            while i < (len(contenu)):
                self.pbEtape2.setValue(cptPb)
                rowTmp = contenu[i].split(';')
                if len(rowTmp[2]) == 0 or len(rowTmp[1]) == 0:
                    cptVide += 1
                    ligneVide.append(rowTmp)
                    contenu.remove(contenu[i])

                elif len(rowTmp[5]) < 1 and len(rowTmp[6]) < 1 and len(rowTmp[7]) < 1 :
                    cptInfo += 1
                    ligneVide.append(rowTmp)
                    contenu.remove(contenu[i])
                else:
                    i += 1
                cptPb += incPb

            self.pbEtape2.setValue(cptPb)
            msg = u"Le fichier contient %i lignes erronées :\n" % (cptVide + cptExist + cptInfo)
            msg += u"   - Il y a %i lignes sans date\n" % (cptVide)
            msg += u"   - Il y a %i lignes sans information\n" % (cptInfo)
            msg += u"   - Il y a %i lignes déjà présentes dans la base\n" % (cptExist)
            msg += u"Il reste %i lignes à insérer\n" % (len(contenu))
            QMessageBox.information(QWidget(), u"Informations sur le contenu du fichier", msg)
            self.btnLancementEtape2.setEnabled(False)

            self.obs_a_inserer = contenu
            if len(contenu) > 0:
                self.btnLancementEtape3.setEnabled(True)

    def lancementEtape3(self):
        #Fonction de lancement de l'étape 3
        #Parcours les données bonnes à l'insertion et les inserts dans la base
        if len(self.obs_a_inserer) > 0:
            db, dbSchema = self.connexion()

            if (not db.open()):
                QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                     QMessageBox.Ok)
            else:
                contenu = self.obs_a_inserer
                cptPb = 1.0
                incPb = 100.0 / float(len(contenu))
                nbRowInser = 0
                nbRowExist = 0
                for row in contenu:
                    self.pbEtape3.setValue(cptPb)
                    row = row.split(';')
                    #Récupération des données intéressantes
                    date = row[1]
                    if len(row[2]) > 0:
                        heure = row[2] + ":00:00"

                    if len(row[5]) > 0:
                        temp = row[5].replace(",", ".")
                    else:
                        print row[5]
                        temp = None

                    if len(row[6]) > 0:
                        vent = row[6].replace(",", ".")
                    else:
                        print row[6]
                        vent = None

                    if len(row[7]) > 0:
                        dvent = row[7]
                    else:

                        print row[7]
                        dvent = None

                    try:
                        nebu = int(row[8])
                    except:
                        nebu = None

                    datetime = date + " " + heure
                    #Préparationd e la requête d'insertion et insertion
                    queryInsMeteo = QSqlQuery(db)
                    wrelation = dbSchema + ".meteo"
                    queryInsMeteo.prepare("INSERT INTO brut.meteo (met_date_time, met_temperature, met_vent, met_directionv, met_nebulosite) VALUES (?, ?, ?, ?, ?)")

                    queryInsMeteo.addBindValue(datetime)
                    queryInsMeteo.addBindValue(temp)
                    queryInsMeteo.addBindValue(vent)
                    queryInsMeteo.addBindValue(dvent)
                    queryInsMeteo.addBindValue(nebu)
                    if not queryInsMeteo.exec_():
                        if u"la valeur d'une clé dupliquée rompt la contrainte unique « uq_meteo »" in queryInsMeteo.lastError().text():
                            nbRowExist += 1
                        else:
                            QMessageBox.critical(self, u"Erreur - Insertion Météo", queryInsMeteo.lastError().text(),QMessageBox.Ok)

                    else:
                        nbRowInser += 1
                    cptPb += incPb
                QMessageBox.information(self, u'Information - Insertion Observation',u"%i lignes ont été  intégrée\n %i lignes étaient déjà présentes." % (nbRowInser, nbRowExist))

    def connexion(self):
        #FOnction de connexion à la base
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





