# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Export des données pour le logger analyseur
import sys
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *


from forms.export_logger import *

import codecs

class ExportLoggerDialog(QDialog, Ui_export_logger):
    #Classe de lancement de la fenêtre logger
    def __init__(self,parent = None):
        #Initialisation de la fenêtre
        super(ExportLoggerDialog, self).__init__(parent)

        self.setupUi(self)

        self.mapper = None

        self.pb_export.setEnabled(False)

        self.db, self.dbSchema = self.connexion()

        #Connexion des boutons eurs actions
        self.connect(self.pb_export, SIGNAL("clicked()"), self.creation_csv)
        self.connect(self.pb_quitter, SIGNAL("clicked()"), self.accept)
        self.connect(self.pb_recherche, SIGNAL("clicked()"), self.definir_repertoire)

        self.listDon = []#Liste initialisé pour la récupération des lignes

        # combo district :
        #Récupération des données de la base pour la combobox
        self.db.open()
        wrelation = self.dbSchema + ".district_capture"
        self.relation_district = QSqlTableModel(self, self.db)
        self.relation_district.setTable(wrelation)
        self.relation_district.select()

        self.cb_liste.setModel(self.relation_district)
        self.cb_liste.setModelColumn(self.relation_district.fieldIndex("distr_nom"))
        # self.cb_liste.setModelColumn(self.relation_district.fieldIndex("distr_id"))
        # self.cb_liste.setColumnHidden(self.relation_district.fieldIndex("distr_id"), True)



    def definir_repertoire(self):
        #Définition du chemin du fichier où exporter les données
        repertoire = QFileDialog.getSaveFileName(self, u"Sélectionner le répertoire où enregistrer le fichier", "C:\Users\Antoine\Documents\projet_tut\TEST_EXPORT", "Logger(*.csv)")
        if repertoire != "":
            self.lbl_chemin.setText(repertoire)
            self.pb_recherche.setEnabled(True)
            self.repertoireChoisi = repertoire
            self.pb_export.setEnabled(True)
        else:
            self.repertoireChoisi = repertoire
            if self.repertoireChoisi == "":
                QMessageBox.information(self, u'Information', u'Aucune(s) information(s) saisie(s) !')
                self.pb_recherche.setEnabled(True)

    def recuperation_donnee (self):
        #Fonction de récupération des données en fonction des choix
        self.listDon = []
        db, dbSchema = self.connexion()

        #COnnexion à la base de données
        if (not db.open()):

            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données principale ...",
                                 QMessageBox.Ok)

        else:
            #Test des différents choix possible
            if (self.cb_liste.currentText()) != "All":
                #Requête sur tous les champs
                queryId = QSqlQuery(db)
                queryId.prepare("select ind_log, extract (YEAR from obs_date), extract (MONTH from obs_date), extract (DAY from obs_date),extract (HOUR from obs_heure), extract (MINUTE from obs_heure), extract (SECOND from obs_heure), ST_Y(obs_geom) AS Latitude, ST_X(obs_geom) AS Longitude, obs_speed, obs_searching_time, obs_gps_voltage, obs_gps_temperature, '' as altitude, '' as Div_up, '' as Div_down, '' as NoGPS_timeout, '' as NoGPS_diving, '' as In_range, '' as Diving_duration, '' as Raw_latitude, '' as Raw_long FROM brut.observation, brut.individu, brut.district_capture where obs_ind_id = ind_id and distr_id = ind_distr_id and distr_nom = ? ")
                queryId.addBindValue(self.cb_liste.currentText())

                if queryId.exec_():
                    while queryId.next():
                        ligne = str(queryId.value(0)) + ";" + str(queryId.value(1)) + ";" + str(queryId.value(2)) + ";" + str(queryId.value(3)) + ";" + str(queryId.value(4)) + ";" + str(queryId.value(5)) + ";" + str(queryId.value(6))+ ";" + str(queryId.value(7)) + ";"+ str(queryId.value(8)) + ";"+ str(queryId.value(9)) + ";"+ str(queryId.value(10)) + ";"+ str(queryId.value(11)) + ";"+ str(queryId.value(12)) + ";"+ str(queryId.value(13)) + ";"+ str(queryId.value(14))+ ";"+ str(queryId.value(15))+ ";"+ str(queryId.value(16))+ ";"+ str(queryId.value(17))+ ";"+ str(queryId.value(18))+ ";"+ str(queryId.value(19))+ ";"+ str(queryId.value(20))+ ";"+ str(queryId.value(21))+"\n"
                        self.listDon.append(ligne)

            else:
                #Requête selon le district
                queryAll = QSqlQuery(db)
                queryAll.prepare("select ind_log, extract (YEAR from obs_date), extract (MONTH from obs_date), extract (DAY from obs_date),extract (HOUR from obs_heure), extract (MINUTE from obs_heure), extract (SECOND from obs_heure), ST_Y(obs_geom) AS Latitude, ST_X(obs_geom) AS Longitude, obs_speed, obs_searching_time, obs_gps_voltage, obs_gps_temperature, '' as altitude, '' as Div_up, '' as Div_down, '' as NoGPS_timeout, '' as NoGPS_diving, '' as In_range, '' as Diving_duration, '' as Raw_latitude, '' as Raw_long FROM brut.observation, brut.individu where obs_ind_id = ind_id")
                if queryAll.exec_():
                    while queryAll.next():
                        ligne = str(queryAll.value(0)) + ";" + str(queryAll.value(1)) + ";" + str(queryAll.value(2)) + ";" + str(queryAll.value(3)) + ";" + str(queryAll.value(4)) + ";" + str(queryAll.value(5)) + ";" + str(queryAll.value(6))+ ";" + str(queryAll.value(7)) + ";"+ str(queryAll.value(8)) + ";"+ str(queryAll.value(9)) + ";"+ str(queryAll.value(10)) + ";"+ str(queryAll.value(11)) + ";"+ str(queryAll.value(12)) + ";"+ str(queryAll.value(13)) + ";"+ str(queryAll.value(14))+ ";"+ str(queryAll.value(15))+ ";"+ str(queryAll.value(16))+ ";"+ str(queryAll.value(17))+ ";"+ str(queryAll.value(18))+ ";"+ str(queryAll.value(19))+ ";"+ str(queryAll.value(20))+ ";"+ str(queryAll.value(21))+"\n"
                        self.listDon.append(ligne)


    def creation_csv (self):
        #Fonction de création du fichier
        self.recuperation_donnee()#Appel de la sélection des données

        entetes = [
            u'Logger ID',
            u'Year',
            u'Month',
            u'Day',
            u'Hour',
            u'Minute',
            u'Second',
            u'Latitude',
            u'Longitude',
            u'Speed',
            u'Searching time',
            u'Voltage',
            u'Temperature',
            u'Altitude',
            u'Div up',
            u'Div down',
            u'No GPS - timeout',
            u'No GPS - diving',
            u'In range',
            u'Diving duration',
            u'Raw latitude',
            u'Raw',
        ]

        contenu = self.listDon
        cpt_row_inserer = 0
        cptPb = 1.0
        incPb = 100.0 / float(len(contenu))
        f = codecs.open(self.lbl_chemin.text(), mode='w', encoding='utf-8')
        ligneEntete = ";".join(entetes) + "\n"
        f.write(ligneEntete)
        for row1 in contenu:
            #Parcours de la liste et insértion dans le fichier
            row = row1.replace(".0;", ";")
            row = row.replace(";0.0", ";")
            self.pb_logger.setValue(cptPb)
            cptPb += incPb
            f.write(row)
            cpt_row_inserer +=1
        f.close()

        msg = u"Vous venez d'exporter %i lignes pour le Logger." % cpt_row_inserer
        QMessageBox.information(QWidget(), u"Informations sur l'export", msg)





    def reject(self):
        self.accept()

    def accept(self):
        self.db.close()
        QDialog.accept(self)

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

class DistrictsDelegate(QSqlRelationalDelegate):
    def __init__(self, parent=None):
        super(DistrictsDelegate, self).__init__(parent)

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