# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Export pour movebank

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.export_movebank import *

import codecs


class ExportMovebankDialog(QDialog, Ui_export_movebank):
    #CLasse d'initialisation de la fenêtre d'export movbank
    def __init__(self, parent = None):
        #Initialisation des ètres
        super(ExportMovebankDialog, self).__init__(parent)
        self.setupUi(self)

        self.pb_export.setEnabled(False)
        self.dteDebut.setEnabled(False)
        self.dteFin.setEnabled(False)

        self.total = False
        #Création des connexions aux boutons/actions
        self.connect(self.pb_export, SIGNAL("clicked()"), self.creation_csv)
        self.connect(self.pb_quitter, SIGNAL("clicked()"), self.accept)
        self.connect(self.pb_recherche, SIGNAL("clicked()"), self.definir_repertoire)
        self.connect(self.rb_periode, SIGNAL("clicked()"), self.radioPeriode)
        self.connect(self.rb_zone, SIGNAL("clicked()"), self.radioListe)

        self.listDon = []
    def definir_repertoire(self):
        #Récupération du chemin du fichier où enregistrer les infos
        repertoire = QFileDialog.getSaveFileName(self, u"Sélectionner le répertoire ainsi que le nom du fichier à enregistrer", "C:\Téléchargements\TEST_EXPORT", "Movebank(*.csv)")
        if repertoire != "":
            self.lbl_chemin.setText(repertoire)
            self.pb_recherche.setEnabled(True)
            self.pb_export.setEnabled(True)

        else:
            self.repertoireChoisi = repertoire
            if self.repertoireChoisi == "":
                QMessageBox.information(self,u'Information', u'Aucune(s) information(s) saisie(s) !')
                self.pb_recherche.setEnabled(True)


    def recuperation_donnee (self):
        #Récupération des infos à enregistrer
        self.listDon = []
        db, dbSchema = self.connexion()
        #Récupération des périodes
        dateDebut = str(self.dteDebut.date().day()) +"/" + str(self.dteDebut.date().month()) +"/"+ str(self.dteDebut.date().year())
        dateFin = str(self.dteFin.date().day()) +"/"+ str(self.dteFin.date().month()) +"/"+ str(self.dteFin.date().year())

        if (not db.open()):
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...", QMessageBox.Ok)
        else:
            #Connexion à la base de données
            queryIns = QSqlQuery(db)
            #Création et exécution des requêtes selon les choix
            if self.total :
                queryIns.prepare( "SELECT esp_nom_latin, ind_log, '' AS Nom_oiseau, to_char(obs_date,'dd/mm/yyyy'), to_char(obs_heure, 'hh:min:ss'), ST_Y(obs_geom) AS Latitude, ST_X(obs_geom) AS Longitude FROM brut.observation, brut.espece, brut.individu WHERE obs_ind_id = ind_id and ind_esp_id = esp_id")

            else:
                queryIns.prepare("SELECT esp_nom_latin, ind_log, '' AS Nom_oiseau, to_char(obs_date,'dd/mm/yyyy'), to_char(obs_heure, 'hh:min:ss'), ST_Y(obs_geom) AS Latitude, ST_X(obs_geom) AS Longitude FROM brut.observation, brut.espece, brut.individu WHERE obs_ind_id = ind_id and ind_esp_id = esp_id and obs_date between ? and ? ")
                queryIns.addBindValue(dateDebut)
                queryIns.addBindValue(dateFin)
            if queryIns.exec_():
                while queryIns.next():
                    ligne = queryIns.value(0) + ";" + queryIns.value(1)+ ";" + queryIns.value(2)+ ";" +queryIns.value(3)+ ";" +queryIns.value(4)+ ";" +str(queryIns.value(5))+ ";" +str(queryIns.value(6))+ "\n"
                    self.listDon.append(ligne)

    def creation_csv (self):
        #Fonction d'exriture et création du fichier
        self.recuperation_donnee()
        entetes = [
            u'Espece',
            u'Nom GPS',
            u'Nom de l\'oiseau',
            u'Date',
            u'Heure',
            u'Latitude',
            u'Longitude',
        ]

        contenu = self.listDon
        cpt_row_inserer = 0
        cptPb = 1.0
        incPb = 100.0 / float(len(contenu))
        f = codecs.open(self.lbl_chemin.text(), mode ='w', encoding = 'utf-8')
        ligneEntete = ";".join(entetes) + "\n"
        f.write(ligneEntete)
        for row in contenu:
            #Parcours des lignes à insérer et import dans le fichier
            row = row.split(";")
            row[4] = row[4].replace("n", "")
            row = ";".join(row)
            self.pb_movebank.setValue(cptPb)
            cptPb += incPb
            f.write(row)
            cpt_row_inserer += 1
        f.close()
        msg = u"Vous venez d'exporter %i lignes pour Movebank." % cpt_row_inserer
        QMessageBox.information(QWidget(), u"Informations sur l'export", msg)


    def radioPeriode(self):
        #Fonction d'affichage caché pour les exports par période
        self.dteDebut.setEnabled(True)
        self.dteFin.setEnabled(True)
        print(self.dteFin.date().year())
        print(self.dteDebut.date().month())
        print(self.dteDebut.date().day())
        self.total = False

    def radioListe(self):
        #Fonction d'affichage caché pour les exports totaux
        self.dteDebut.setEnabled(False)
        self.dteFin.setEnabled(False)
        self.total = True

    def reject(self):
        self.accept()

    def accept(self):
        QDialog.accept(self)

    def connexion(self):
        #Connexion à la base
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

