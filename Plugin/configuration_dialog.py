# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Configuration de la connexion à la base
import sys 
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *

from forms.configuration_form import *

class ConfigurationDialog(QDialog, Ui_configuration_form):
    #Classe de lancement de la fenêtre de configuration
    def __init__(self, parent=None):
        #Initialisation des champs de la fenêtre
        super(ConfigurationDialog, self).__init__(parent)

        self.setupUi(self)

        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

        self.recupParametre()

    def recupParametre(self):
        #Récupération des anciens paramètres
        #Mise par défaut des autre champs
        s = QSettings()
        self.leHote.setText(s.value("geolimi/config/hote", "localhost"))
        self.lePort.setText(s.value("geolimi/config/port", "5434"))
        self.leNomBd.setText(s.value("geolimi/config/nomBd", "GeoLimi"))
        self.leSchema.setText(s.value("geolimi/config/schema", "brut"))
        self.leUser.setText(s.value("geolimi/config/user", "postgres"))
        self.lePwd.setText(s.value("geolimi/config/pwd", "pgAdmin"))

    def majParametre(self):
        #Récupération des nouveaux paramètres
        s = QSettings()
        s.setValue("geolimi/config/hote", self.leHote.text())
        s.setValue("geolimi/config/port", self.lePort.text())
        s.setValue("geolimi/config/nomBd", self.leNomBd.text())
        s.setValue("geolimi/config/schema", self.leSchema.text())
        s.setValue("geolimi/config/user", self.leUser.text())
        s.setValue("geolimi/config/pwd", self.lePwd.text())

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        self.majParametre()
        QDialog.accept(self)
        
       