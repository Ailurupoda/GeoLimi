# -*- coding: utf-8 -*-

#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Import marées

import sys
import os
import time
import psycopg2
import shutil
import pickle

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.import_periode_form import *

class ImportMareeDialog(QDialog, Ui_import_periode_form):
    def __init__(self, parent = None):
        super(ImportMareeDialog, self).__init__(parent)
        #Initialisation de la fenêtre d'import

        self.setupUi(self)
        self.periode_a_inserer = ""#Création de la liste de données à insérer

        #Connexion des boutons à leurs effets
        self.connect(self.btnSelectionFichier, SIGNAL("clicked()"), self.selectionFichier)
        self.connect(self.btnLancementEtape1, SIGNAL("clicked()"), self.lancementEtape1)
        self.connect(self.btnLancementEtape2, SIGNAL("clicked()"), self.lancementEtape2)
        self.connect(self.btnLancementEtape3, SIGNAL("clicked()"), self.lancementEtape3)
        self.connect(self.btnQuitter, SIGNAL("clicked()"), self.accept)

    def selectionFichier(self):
        #Fonction de sélection du fichier
        #Demande le chemin du fichier à parcourir
        #Active l'étape suivante
        self.btnLancementEtape1.setEnabled(False)
        self.btnLancementEtape2.setEnabled(False)
        self.btnLancementEtape3.setEnabled(False)
        fichier = QFileDialog.getOpenFileName(self, u"Ouvrir un fichier", u"D:/PTUT", "Logger(*.csv)")
        if fichier:
            self.lbl_url_fichier.setText(fichier)
            self.btnLancementEtape1.setEnabled(True)

    def lancementEtape1(self):
        #Fonction de lancement de l'étape 1
        #Parcour le fichier et prend en compte les données hors entête et hors ligne vide
        #Informe sur le nombre de lignes à parcourir ainsi que le nombre de colonnes contenues
        self.btnLancementEtape2.setEnabled(False)
        self.btnLancementEtape3.setEnabled(False)
        fichier_periode = open(self.lbl_url_fichier.text(), "rb")
        contenu = fichier_periode.read()
        contenu = contenu.split('\n')
        listRemov = [contenu[0]]
        col = contenu[0].split(';')
        cptPb = 1.0
        incPb = 100.0/float(len(contenu))
        for row in contenu:
            self.pbEtape1.setValue(cptPb)
        # Si pas de ";" il supprime ( = ligne completement vide)
            if ';' not in row:
                listRemov.append(row)
            else:
                cptPb += incPb
        for rem in listRemov:
            contenu.remove(rem)

        msg = u"Le fichier sélectionné contient %i colonnes et %i lignes à insérer." % (len(col), len(contenu))
        QMessageBox.information(QWidget(), u"Informations sur le contenu du fichier", msg)
        fichier_periode.close()
        self.btnLancementEtape2.setEnabled(True)
        self.periode_a_inserer = contenu

    def lancementEtape2(self):
        #Fonction de lancement de l'étape 2
        #Parcours des données en enlevant les données non utilisables (trop d'infos manquantes)
        #Affiche le résultat du parcours
        self.btnLancementEtape3.setEnabled(False)
        contenu = self.periode_a_inserer
        ligneVide = []
        ligneExist = []
        listDate = []

        cptDate = 0
        cptExist = 0
        cptCoef = 0
        cptMaree = 0

        cptPb = 1.0
        incPb = 100.0/float(len(contenu))

        listLog = []

        db, dbSchema = self.connexion()

        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)
        else:

            wrelation = dbSchema + ".maree"
            queryDate = QSqlQuery(db)
            queryDate.prepare("SELECT mar_date FROM brut.maree")
            if queryDate.exec_():
                while queryDate.next():
                     listDate.append(queryDate.value(0))
        i = 0
        while i < (len(contenu)):
            self.pbEtape2.setValue(cptPb)
            rowTmp = contenu[i].split(';')
            if len(rowTmp[0]) == 0:#Colonne date non vide
                cptDate += 1
                ligneVide.append(rowTmp)
                contenu.remove(contenu[i])
            elif len(rowTmp[9]) == 0 and len (rowTmp[10]) == 0:#Colonnes coef non vide
                cptCoef += 1
                ligneVide.append(rowTmp)
                contenu.remove(contenu[i])

            elif len (rowTmp[11]) == 0 and len (rowTmp[13]) == 0 and len (rowTmp[15]) == 0 and len(rowTmp[17]) :#Colonnes heure maree non vide
                cptMaree += 1
                ligneVide.append(rowTmp)
                contenu.remove(contenu[i])
            elif len(rowTmp[12]) == 0 and len(rowTmp[14]) == 0 and len(rowTmp[16]) == 0 and len(rowTmp[18]):#Colonnes hauteur maree non vide
                cptMaree += 1
                ligneVide.append(rowTmp)
                contenu.remove(contenu[i])
            else:
                i += 1
            cptPb += incPb
        msg = u"Le fichier contient %i lignes erronées :\n" % (len(ligneVide) + len(ligneExist) + (cptCoef)+ (cptMaree))
        msg += u"   - Il y a %i lignes sans date\n" % (cptDate)
        msg += u"   - Il y a %i lignes déjà présentes dans la base\n" % (cptExist)
        msg += u"   - Il y a %i lignes sans coefficients et/ou hauteur de marée renseignés\n" % (cptCoef + cptMaree)
        msg += u"Il reste %i lignes à insérer\n" % (len(contenu))
        QMessageBox.information(QWidget(), u"Informations sur le contenu du fichier", msg)

        self.periode_a_inserer = contenu
        self.btnLancementEtape2.setEnabled(False)
        if len(contenu) > 0:
            self.btnLancementEtape3.setEnabled(True)


    def lancementEtape3(self):
        #Fonction de lancement de l'étape 3
        #Parcours les données bonnes à l'insertion et les inserts dans la base
        trouve = True
        precM = ''#Initialisation de la marée précédente (Pour déterminer l'inter marée entre 2 jours)
        if len(self.periode_a_inserer) > 0:
            db, dbSchema = self.connexion()
            #Connexion à la base
            if (not db.open()):
                QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...", QMessageBox.Ok)
            else:
                    #Récupération des lignes à parcourir
                    contenu = self.periode_a_inserer
                    cptPb = 1.0
                    incPb = 100.0 / (float(len(contenu))) #Préparation de la bar de progression
                    nbRowInser = 0
                    nbRowExist = 0
                    for row in contenu:
                        #Parcours des données à insérer
                        listMar = []
                        row = row.split(';')

                        date = row[0]
                        #Récupération des date time pour chaque marées
                        bm1D = date + ' ' + row[11] + ':00'
                        bm2D = date + ' ' + row[15] + ':00'
                        bh1D = date + ' ' + row[13] + ':00'
                        bh2D = date + ' ' + row[17] + ':00'

                        #Récupération des coeficients matin et soir
                        coef_matin = row[9]
                        coef_soir = row[10]


                        #Récupération des hauteurs de marées lorsqu'elles existent (remplacement des , par des .)
                        if len(row[12])>0:
                            hauteur_bm_1 = float(row[12].replace(',', '.'))
                        else :
                            hauteur_bm_1 = None
                        if len(row[16])>0:
                            hauteur_bm_2 = float(row[16].replace(',', '.'))
                        else :
                            hauteur_bm_2 = None
                        if len(row[14])>0:
                            hauteur_hm_1 = float(row[14].replace(',', '.'))
                        else :
                            hauteur_hm_1 = None
                        if len(row[18])>0:
                            hauteur_hm_2 = float(row[18].replace(',', '.'))
                        else :
                            hauteur_hm_2 = None

                        #Affectation du coeficient matin ou soir
                        if int(row[11][0:2]) < int(row[15][0:2]):
                                coef_mb1 = int(coef_matin)
                                coef_mb2 = int(coef_soir)
                        else:
                            coef_mb1 = int(coef_soir)
                            coef_mb2 = int(coef_matin)

                        try:
                            #Test si il y a 3 ou 4 marées
                            if int(row[13][0:2]) < int(row[17][0:2]):
                                coef_mh1 = int(coef_matin)
                                coef_mh2 = int(coef_soir)
                            else:
                                coef_mh1 = int(coef_soir)
                                coef_mh2 = int(coef_matin)

                            #Si 4 marées alors on regarde combien on en avait avant
                            trouve_prec = trouve#Récupération de la données précédente
                            trouve = True#Initialisation à 4 marées présentes

                        except:
                            #Si 3 marées dans la journées
                            trouve_prec = trouve#Récupèration du nombre de marées de la veille
                            trouve = False#Initialisation du nombre de marées du jour à 3
                            coef_mh1 = int(coef_soir)#Le coeficient de la première marée haute est celui du matin
                            coef_mh2 = int(coef_matin)#Le coeficient de la 2 eme marée haute est celui du soir


                        if trouve_prec :
                            #Si on était précédement sur 4 marées
                            #On paramètre les données des 2 marées basse et de la première marée haute
                            #On paramètre les marées entre la BM1 et la HM1 et la HM1 et la BM2
                            listMar.append((bm1D, bm1D, hauteur_bm_1, coef_mb1, 2))
                            listMar.append((bm1D, bh1D, 0, coef_mb1, 3))
                            listMar.append((bh1D, bh1D, hauteur_hm_1, coef_mh1, 1))
                            listMar.append((bh1D, bm2D, 0, coef_mh1, 4))
                            listMar.append((bm2D, bm2D, hauteur_bm_2, coef_mb2, 2))

                            if trouve:
                                #Si on est suur un jour à 4 marées
                                #On ajoute la MH2
                                #On ajoute l'inter marée MB2/HM2
                                listMar.append((bh2D, bh2D, hauteur_hm_2, coef_mh2, 1))
                                listMar.append((bm2D, bh2D, 0, coef_mb2, 3))
                                if len(precM) > 0:
                                    #Si on a une marée précédente, on ajoute l'inter marée entre celle du jour précédent et la première marée du jour actuel
                                    listMar.append((precM, bm1D, 0, coef_mh2, 4))
                                precM = bh2D#On récupère la dernière marée de la journée
                            else:
                                #Si on est sur un jour à 3 marées
                                #On va seulement intégrer le dernier inter marée
                                if len(precM) > 0:
                                    #Si on a une marée précédente, on ajoute l'inter marée avec le jour précédent
                                    listMar.append((precM, bm1D, 0, coef_mb2, 3))
                                precM = bm2D#Récupération de la dernière marée

                        else:
                            #Si le jour précédent n'avait que 3 marées
                            #On prépare toutes les marées du jour dans l'ordre (On commence par une marée haute)
                            listMar.append((bh1D, bh1D, hauteur_hm_1, coef_mh1, 1))
                            listMar.append((bh1D, bm1D, 0, coef_mh1, 4))
                            listMar.append((bm1D, bm1D, hauteur_bm_1, coef_mb1, 2))
                            listMar.append((bm1D, bh2D, 0, coef_mb1, 3))
                            listMar.append((bh2D, bh2D, hauteur_hm_2, coef_mh2, 1))
                            listMar.append((bh2D, bm2D, 0, coef_mh2, 4))
                            listMar.append((bm2D, bm2D, hauteur_bm_2, coef_mb2, 2))
                            if len(precM) > 0:
                                listMar.append((precM, bh1D, 0, coef_mb2, 3))
                            precM = bm2D#Récupération de la dernière marée à inserer

                        #Préparation de la requete d'insertion
                        queryMar = QSqlQuery(db)
                        wrelation = dbSchema + ".maree"
                        queryMar.prepare("INSERT INTO " + wrelation + " (mar_date_time_p1, mar_date_time_p2, mar_coef, mar_marnage, mar_tymar_id) VALUES (?, ?, ?, ?, ?)")

                        for key in listMar:
                            # Parcours de la liste de ligne à insérer
                            queryMar.addBindValue(key[0])
                            queryMar.addBindValue(key[1])
                            queryMar.addBindValue(key[3])
                            queryMar.addBindValue(key[2])
                            queryMar.addBindValue(key[4])
                            if not queryMar.exec_():
                                if u"la valeur d'une clé dupliquée rompt la contrainte unique « uq_maree »" in queryMar.lastError().text():
                                    nbRowExist += 1
                                    #Echapement des données déjà insérées
                                else:
                                    #Affichage de l'erreur SQL posant probleme
                                    QMessageBox.critical(self, u"Erreur - Insertion Observation", queryMar.lastError().text(), QMessageBox.Ok)
                            else:
                                nbRowInser += 1
                            cptPb += (incPb / len(listMar))
                            self.pbEtape3.setValue(cptPb)
                    #Récapitulatif des données insérées
                    QMessageBox.information(self, u'Information - Insertion Observation', u"%i lignes ont été  intégrées\n %i lignes étaient déjà présentes." % (nbRowInser, nbRowExist))


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





