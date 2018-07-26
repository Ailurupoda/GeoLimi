# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Chargement des données à la carte
import sys 
import os
import sqlite3

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *

from forms.load_data_form import *

class LoadDataDialog(QDialog, Ui_load_data_form):
    #Classe de lancement de la fenêtre de chargement des données
    def __init__(self, parent=None):
        #Initialisation des champs de la fenêtre
        super(LoadDataDialog, self).__init__(parent)

        self.setupUi(self)
        self.getStyleList()

        self.btnCharger.clicked.connect(self.charger)
        self.bboxFermer.rejected.connect(self.reject)

        #Création des groupes à afficher à la carte
        self.qgisGeolimiLayerList = [
            {'db': '', 'groupe': u'Observations', 'label': u'Observation', 'name': 'observation', 'table': 'observation', 'geom': 'obs_geom', 'sql': '', 'key': 'obs_id'},

            {'db': '', 'groupe': u'Paramètres', 'label': u'Age', 'name': u'Age', 'table': 'age', 'geom': None, 'sql': '', 'key': 'age_id'},
            {'db': '', 'groupe': u'Paramètres', 'label': u'Cycle biologique', 'name': u'Cycle biologique', 'table': 'cycle_biologique', 'geom': None, 'sql': '', 'key': 'cycle_id'},
            {'db': '', 'groupe': u'Paramètres', 'label': u'District de capture', 'name': u'District de capture', 'table': 'district_capture', 'geom': None, 'sql': '', 'key': 'distr_id'},
            {'db': '', 'groupe': u'Paramètres', 'label': u'Espèce', 'name': u'Espèce', 'table': 'espece', 'geom': None, 'sql': '', 'key': 'esp_id'},
            {'db': '', 'groupe': u'Paramètres', 'label': u'Fichier', 'name': u'Fichier', 'table': 'fichier', 'geom': None, 'sql': '', 'key': 'fich_id'},
            {'db': '', 'groupe': u'Paramètres', 'label': u'Individu', 'name': u'Individu', 'table': 'individu', 'geom': None, 'sql': '', 'key': 'ind_id'},
            {'db': '', 'groupe': u'Paramètres', 'label': u'Logger', 'name': u'Logger', 'table': 'ancien_logger', 'geom': None, 'sql': '', 'key': 'anc_log_id'},

            {'db': '', 'groupe': u'Divers', 'label': u'Type d\'activité', 'name': u'Type d\'activité', 'table': 'type_activite', 'geom': None, 'sql': '', 'key': 'type_act_id'},
            {'db': '', 'groupe': u'Divers', 'label': u'Type de marée', 'name': u'Type de marée', 'table': 'type_maree', 'geom': None, 'sql': '', 'key': 'tymar_id'},
            {'db': '', 'groupe': u'Divers', 'label': u'Type de soleil', 'name': u'Type de soleil', 'table': 'type_soleil', 'geom': None, 'sql': '', 'key': 'type_sol_id'}
        ]

        self.totalSteps = 0
        self.step = 0

    def getStyleList(self):
        #Récupération du style à charger
        spath = os.path.join(os.path.dirname(__file__), "styles/")
        dirs = os.listdir(spath)
        dirs = [a for a in dirs if os.path.isdir(os.path.join(spath, a))]
        dirs.sort()
        self.cmbTheme.clear()
        for d in dirs:
            self.cmbTheme.addItem('%s' % d, d)
        
    def charger(self):
        #Chargement des données à la carte
        nomRoot = "Geolimi"
        s = QSettings()

        hote = s.value("geolimi/config/hote", "localhost")
        port = s.value("geolimi/config/port", "5434")
        db = s.value("geolimi/config/nomBd", "GeoLimi")
        schema = s.value("geolimi/config/schema", "brut")
        user = s.value("geolimi/config/user", "postgres")
        pwd = s.value("geolimi/config/pwd", "postgres")

        root = QgsProject.instance().layerTreeRoot()

        if root.findGroup("Geolimi"):
            QMessageBox.critical(self, "Erreur", u"Les données de cette connexion sont déjà chargées ...", QMessageBox.Ok)
        else:
            QApplication.setOverrideCursor(Qt.WaitCursor)
            g0 = root.insertGroup(0, nomRoot)
            g1 = g0.addGroup(u"Observations")
            g2 = g0.addGroup(u"Paramètres")
            g3 = g0.addGroup(u"Divers")

            self.totalSteps = len(self.qgisGeolimiLayerList)

            for x in self.qgisGeolimiLayerList:
                uri = QgsDataSourceURI()
                uri.setConnection(hote, port, db, user, pwd)
                uri.setDataSource(schema, x["table"], x["geom"])
                une_couche = QgsVectorLayer(uri.uri(), x["name"], "postgres")

                if une_couche.isValid():
                    # style
                    if x["geom"]:
                        qmlPath = os.path.join(os.path.dirname(__file__), "styles/%s/%s.qml" % (self.cmbTheme.currentText(), x['name']))
                        if os.path.exists(qmlPath):
                            une_couche.loadNamedStyle(qmlPath)

                    groupe = g0.findGroup(x["groupe"])
                    QgsMapLayerRegistry.instance().addMapLayer(une_couche, False)
                    l = groupe.addLayer(une_couche)
                    if x["geom"]:
                        l.setExpanded(True)
                    l.setCustomProperty("nomOrigine", x["table"])

                else:
                    QMessageBox.critical(self, "Erreur", u"Source de données (%s) non valide ..." %(x["name"]),  QMessageBox.Ok)
                self.step += 1
                self.updateProgressBar()

            g0.setExpanded(True)
            g1.setExpanded(True)
            g2.setExpanded(False)
            g3.setExpanded(False)

            QApplication.restoreOverrideCursor()
            self.reject()

    def updateProgressBar(self):
        self.pbProcess.setValue(int(self.step * 100 / self.totalSteps))

    def reject(self):
        QDialog.reject(self)
        

        
       