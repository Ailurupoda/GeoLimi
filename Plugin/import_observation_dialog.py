# -*- coding: utf-8 -*-

#Antoine Blain, COrentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Import des observations

import sys 
import os
import time
import psycopg2
import shutil
import pickle

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from qgis.gui import *

from forms.import_observation_form import *

class ImportObservationDialog(QDialog, Ui_import_observation_form):
    def __init__(self, parent = None):
        super(ImportObservationDialog, self).__init__(parent)
        # Initialisation de la fenêtre d'import

        self.setupUi(self)


        self.obs_a_inserer = ""
        self.obs_goel = []
        self.entete = ""

        self.btnSelectionGoel.setEnabled(False)

        # Connexion des boutons à leurs effets
        self.connect(self.btnSelectionFichier, SIGNAL("clicked()"), self.selectionFichier)
        self.connect(self.btnLancementEtape1, SIGNAL("clicked()"), self.lancementEtape1)
        self.connect(self.btnLancementEtape2, SIGNAL("clicked()"), self.lancementEtape2)
        self.connect(self.btnLancementEtape3, SIGNAL("clicked()"), self.lancementEtape3)
        self.connect(self.btnSelectionGoel, SIGNAL("clicked()"), self.selectionGoeland)

        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def selectionFichier(self):
        # Fonction de sélection du fichier
        # Demande le chemin du fichier à parcourir
        # Active l'étape suivante
        self.btnLancementEtape1.setEnabled(False)
        self.btnLancementEtape2.setEnabled(False)
        self.btnLancementEtape3.setEnabled(False)
        fichier = QFileDialog.getOpenFileName(self, u"Ouvrir un fichier", u"D:\PTUT", "Logger(*.csv)")
        if fichier:
            self.lbl_url_fichier.setText(fichier)
            self.btnLancementEtape1.setEnabled(True)

    def selectionGoeland(self):
        # Fonction de sélection du dans lequel insérer les goelands trouvés
        # Demande le nom du fichier goeland
        # Active l'étape suivante
        fichier = QFileDialog.getSaveFileName(self, u"Choisir un fichier de sauvegarde", u"D:\PTUT", "Fichier Goeland (*.csv)")
        if fichier:
            self.lbl_url_goeland.setText(fichier)
            self.btnLancementEtape3.setEnabled(True)

    def lancementEtape1(self):
        # Fonction de lancement de l'étape 1
        # Parcour le fichier et prend en compte les données hors entête et hors ligne vide
        # Informe sur le nombre de lignes à parcourir ainsi que le nombre de colonnes contenues
        self.btnLancementEtape2.setEnabled(False)
        self.btnLancementEtape3.setEnabled(False)
        fichier_obs = open(self.lbl_url_fichier.text(), "rb")
        contenu = fichier_obs.read()
        contenu = contenu.split('\n')
        listRemov = [contenu[0]]
        self.entete = contenu[0]
        col = contenu[0].split(';')
        cptPb = 1.0
        incPb = 100.0/float(len(contenu))
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
        #/!\ Les goelands sont les loggers qui ne sont pas présents dans la base/!\
        self.btnLancementEtape3.setEnabled(False)
        contenu = self.obs_a_inserer

        ligneVide = []
        ligneGoel = []
        ligneExist = []

        cptGoel = 0
        cptLog = 0
        cptDate = 0
        cptGeom = 0
        cptExist = 0

        cptPb = 1.0
        incPb = 100.0/float(len(contenu))

        listLog = []

        db, dbSchema = self.connexion()

        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...", QMessageBox.Ok)
        else:

            wrelation = dbSchema + ".individu"
            queryLog = QSqlQuery(db)
            queryLog.prepare("SELECT ind_log FROM brut.individu")
            if queryLog.exec_():
                while queryLog.next():
                     listLog.append(queryLog.value(0))

            queryExist = QSqlQuery(db)
            queryExist.prepare("SELECT obs_id FROM brut.observation o JOIN brut.individu i on o.obs_ind_id = i.ind_id  WHERE obs_geom = ? and obs_date = ? and obs_heure = ? and ind_log = ? ")
            i = 0
            while i < (len(contenu)):
                #Parcours des données et supression des lignes inutiles
                #Création d'une liste de goeland quand ils sont trouvés
                self.pbEtape2.setValue(cptPb)
                rowTmp = contenu[i].split(';')
                if len(rowTmp[0]) < 0:
                    cptLog += 1
                    ligneVide.append(rowTmp)
                    contenu.remove(contenu[i])
                elif rowTmp[0] not in listLog:
                    cptGoel += 1
                    ligneGoel.append(contenu[i])
                    contenu.remove(contenu[i])
                elif len(rowTmp[1]) == 0 or len(rowTmp[2]) == 0 or len(rowTmp[3]) == 0 or len(rowTmp[4]) == 0 or len(rowTmp[5]) == 0 or len(rowTmp[6]) == 0:
                    cptDate += 1
                    ligneVide.append(rowTmp)
                    contenu.remove(contenu[i])
                elif len(rowTmp[7]) == 0 or len(rowTmp[8]) == 0:
                    cptGeom += 1
                    ligneVide.append(rowTmp)
                    contenu.remove(contenu[i])
                else:
                    i += 1
                cptPb += incPb
            msg = u"Le fichier contient %i lignes erronées :\n" % (len(ligneVide) + len(ligneGoel) + len(ligneExist))
            msg += u"   - Il y a %i lignes sans logger\n" % (cptLog)
            msg += u"   - Il y a %i lignes sans date\n" % (cptDate)
            msg += u"   - Il y a %i lignes sans coordonnées\n" % (cptGeom)
            msg += u"   - Il y a %i lignes ne conernant pas les limicoles\n" % (cptGoel)
            msg += u"   - Il y a %i lignes déjà présentes dans la base\n" % (cptExist)
            msg += u"Il rest %i lignes à insérer\n" % (len(contenu))
            QMessageBox.information(QWidget(), u"Informations sur le contenu du fichier", msg)

            self.obs_goel = ligneGoel
            self.obs_a_inserer = contenu

            if len(contenu) > 0:
                self.btnLancementEtape3.setEnabled(True)
            if cptGoel > 0:
                self.btnSelectionGoel.setEnabled(True)
                self.btnLancementEtape3.setEnabled(False)


    def lancementEtape3(self):
        x = QSettings()
        # Fonction de lancement de l'étape 3
        # Parcours les données bonnes à l'insertion et les inserts dans la base
        if len(self.obs_a_inserer) > 0:
            db, dbSchema = self.connexion()
            fichId = None

            if (not db.open()):
                QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                     QMessageBox.Ok)
            else:
                print len(self.lbl_url_goeland.text())
                if len(self.lbl_url_goeland.text() ) == 0 :
                    goel = False
                    fGoel = None
                else:
                    goel = True
                    fGoel = self.lbl_url_goeland.text()

                #Requete pour rechercher le fichier que nous parcourons dans la base
                queryIdF = QSqlQuery(db)
                queryIdF.prepare("select fich_id from brut.fichier where fich_chemin = ? ")
                queryIdF.addBindValue(self.lbl_url_fichier.text())
                if queryIdF.exec_():
                    if queryIdF.next():
                        #Récupération de l'id du fichier si il est déjà rpésent
                        fichId = queryIdF.value(0)
                    else:
                        #Sinon, on l'insert et on récupère l'id après
                        queryIns = QSqlQuery(db)
                        wrelation = dbSchema + ".fichier"
                        queryIns.prepare("INSERT INTO " + wrelation + "(fich_chemin, fich_goel, fich_goel_chemin) VALUES (?,?,?)")
                        queryIns.addBindValue(self.lbl_url_fichier.text())
                        queryIns.addBindValue(goel)
                        queryIns.addBindValue(fGoel)
                        if not queryIns.exec_():
                            QMessageBox.critical(self, u"Erreur - Insertion fichier", queryIns.lastError().text(), QMessageBox.Ok)
                        else :
                            requeteOk = True
                if fichId != None or requeteOk:
                    #SI on a bien récupéré l'id du fichier ou inséré le fichier
                    self.fichierGoel(self.obs_goel)
                    queryIdObs = QSqlQuery(db)
                    queryIdObs.prepare("select nextval('brut.observation_obs_id_seq') ")
                    if queryIdObs.exec_():
                        if queryIdObs.next():
                            beforeObs = queryIdObs.value(0)
                            x.setValue("geolimi/id", beforeObs)

                    #Récupération de l'id du fichier
                    queryIdF = QSqlQuery(db)
                    queryIdF.prepare("select fich_id from brut.fichier where fich_chemin = ? ")
                    queryIdF.addBindValue(self.lbl_url_fichier.text())
                    if queryIdF.exec_():
                        if queryIdF.next():
                            fichId = queryIdF.value(0)

                            contenu = self.obs_a_inserer
                            cptPb = 1.0
                            incPb = 100.0 / float(len(contenu))
                            nbRowInser = 0
                            nbRowExist = 0
                            for row in contenu:
                                #Parcours des lignes à insérer
                                self.pbEtape3.setValue(cptPb)
                                row = row.split(';')

                                logger = row[0]
                                date = row[1] + "-" + row[2] +"-"+ row[3]
                                heure = row[4]+":"+row[5]+":"+ row[6]
                                lat= row[7]
                                long = row[8]
                                if len(row[9]) > 0:
                                    speed = row[9]
                                else:
                                    speed = None
                                if len(row[10]) > 0:
                                    search = row[10]
                                else:
                                    search = None
                                if len(row[11]) > 0:
                                    volt = row[11]
                                else :
                                    volt = None
                                if len(row[12]) > 0:
                                    temp = row[12]
                                else:
                                    temp = None

                                #Création de la géométrie
                                queryGeom = QSqlQuery(db)
                                queryGeom.prepare("SELECT st_SetSrid(st_makepoint(?,?),4326)")
                                queryGeom.addBindValue(long)
                                queryGeom.addBindValue(lat)
                                if queryGeom.exec_():
                                    if queryGeom.next():
                                        geom = queryGeom.value(0)

                                #Récupération de l'id individu
                                queryInd = QSqlQuery(db)
                                queryInd.prepare("SELECT ind_id From brut.individu where ind_log = ?")
                                queryInd.addBindValue(logger)
                                if queryInd.exec_():
                                    if queryInd.next():
                                        ind = queryInd.value(0)

                                #Insertion des données
                                query = QSqlQuery(db)
                                wrelation = dbSchema + ".observation"
                                query.prepare("INSERT INTO " + wrelation + " (obs_fich_id, obs_ind_id, obs_date, obs_heure, obs_searching_time, obs_gps_voltage, obs_gps_temperature, obs_speed,obs_geom) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)")
                                query.addBindValue(fichId)
                                query.addBindValue(ind)
                                query.addBindValue(date)
                                query.addBindValue(heure)
                                query.addBindValue(search)
                                query.addBindValue(volt)
                                query.addBindValue(temp)
                                query.addBindValue(speed)
                                query.addBindValue(geom)
                                if not query.exec_():
                                    if  u"la valeur d'une clé dupliquée rompt la contrainte unique « uq_obs »" in query.lastError().text():
                                        nbRowExist += 1
                                        #On passe les données qui sont déjà présentes
                                    else :
                                        QMessageBox.critical(self, u"Erreur - Insertion Observation", query.lastError().text(), QMessageBox.Ok)
                                    cptPb += incPb
                                else:
                                    nbRowInser += 1
                                    cptPb += incPb
                            QMessageBox.information(self, u'Information - Insertion Observation', u"%i lignes ont été  intégrée\n %i lignes étaient déjà présentes.  " % (nbRowInser, nbRowExist))
                            # self.close()
                            # if nbRowInser > 0:
                            #     self.selectObs(beforeObs)


    def connexion(self):
        #Fonction de connexion à la base
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

    def fichierGoel(self, goel):
        # Cette fonction se charge d'enregistrer les goelands dans  le fichier
        # Parcours les données déterminées comme goeland
        #Insère dans le fichier saisi par l'utilisateur
        goelF = self.lbl_url_goeland.text()
        fichier_goel = open(goelF, "w")  # On écrase les anciens scores
        # mon_pickler = pickle.Pickler(fichier_scores)
        fichier_goel.write(self.entete)
        for i in goel:
            fichier_goel.write(i)
        fichier_goel.close()
        return goelF


    def reject(self):
        self.accept()


    def accept(self):
        QDialog.accept(self)





