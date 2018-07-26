#-*-coding: utf-8 -*-

#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Import marées

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *
from qgis.core import *
from qgis.utils import iface
import os

from espece_dialog import *
from individu_dialog import *
from cycle_bio_dialog import *
from age_dialog import *
from districts_dialog import *
from visualiseur_fichier_dialog import *
from type_activite_dialog import *
from type_maree_dialog import *
from type_soleil_dialog import *

from import_observation_dialog import *
from import_meteo_dialog import *
from import_maree_dialog import *
from import_lune_dialog import *

from export_logger_dialog import *
from export_movebank_dialog import *

from configuration_dialog import *
from load_data_dialog import *
from about_dialog import *

class Geolimi:
    def __init__(self, iface):
        self.interface = iface

    def initGui(self):
        # la clé du dictionnaire est le nom de la fonction
        # 1er paramètre de la liste : si la fenêtre est active ou non
        # 2ème paramètre de la liste : la fenêtre
        # 3ème paramètre de la liste : si la fenêtre est dockée ou non
        self.dicoFonction = {"a_propos": [False, None, False], "aide": [False, None, False], "configuration": [False, None, False], "chargement": [False, None, False], "espece": [False, None, False], "import_meteo": [False, None, False], "import_lune": [False, None, False], "import_maree": [False, None, False], "import_observation": [False, None, False], "individu": [False, None, True], "cycle_biologique": [False, None, False], "age": [False, None, False], "district_capture": [False, None, False], "fichier": [False, None, False], "type_soleil": [False, None, False], "type_maree": [False, None, False], "type_activite": [False, None, False], "export_logger": [False, None, False], "export_movebank": [False, None, False]}

        x = QSettings()
        x.setValue("geolimi/id", 0)

        # Création des menus
        iconGestion = QIcon(os.path.dirname(__file__) + "/icons/edit.png")
        self.gestion = QMenu(u"Gestion", self.interface.mainWindow())
        self.gestion.setIcon(iconGestion)

        iconImport = QIcon(os.path.dirname(__file__) + "/icons/import.png")
        self.importation = QMenu(u"Import de données", self.interface.mainWindow())
        self.importation.setIcon(iconImport)

        iconExport = QIcon(os.path.dirname(__file__) + "/icons/export.png")
        self.export = QMenu(u"Exports", self.interface.mainWindow())
        self.export.setIcon(iconExport)

        # Actions Gestion
        self.individu_observation = QAction(u"Individus et observations", self.interface.mainWindow())
        QObject.connect(self.individu_observation, SIGNAL("triggered()"), lambda: self.gereFonction("individu"))

        self.age = QAction(u"Ages", self.interface.mainWindow())
        QObject.connect(self.age, SIGNAL("triggered()"), lambda: self.gereFonction("age"))

        self.cycle_biologique = QAction(u"Cycles biologiques", self.interface.mainWindow())
        QObject.connect(self.cycle_biologique, SIGNAL("triggered()"), lambda: self.gereFonction("cycle_biologique"))

        self.district = QAction(u"Districts", self.interface.mainWindow())
        QObject.connect(self.district, SIGNAL("triggered()"), lambda: self.gereFonction("district_capture"))

        self.espece = QAction(u"Espèces", self.interface.mainWindow())
        QObject.connect(self.espece, SIGNAL("triggered()"), lambda: self.gereFonction("espece"))

        self.fichier = QAction(u"Fichiers", self.interface.mainWindow())
        QObject.connect(self.fichier, SIGNAL("triggered()"), lambda: self.gereFonction("fichier"))

        # self.individu = QAction(u"Individus", self.interface.mainWindow())

        self.type_activite = QAction(u"Type d'activité", self.interface.mainWindow())
        QObject.connect(self.type_activite, SIGNAL("triggered()"), lambda: self.gereFonction("type_activite"))

        self.type_maree = QAction(u"Type de marée", self.interface.mainWindow())
        QObject.connect(self.type_maree, SIGNAL("triggered()"), lambda: self.gereFonction("type_maree"))

        self.type_soleil = QAction(u"Type de soleil", self.interface.mainWindow())
        QObject.connect(self.type_soleil, SIGNAL("triggered()"), lambda: self.gereFonction("type_soleil"))


        # Actions Import
        self.import_meteo = QAction(u"Météo", self.interface.mainWindow())
        QObject.connect(self.import_meteo, SIGNAL("triggered()"), lambda: self.gereFonction("import_meteo"))

        self.import_marees = QAction(u"Marées", self.interface.mainWindow())
        QObject.connect(self.import_marees, SIGNAL("triggered()"), lambda: self.gereFonction("import_maree"))

        self.import_lune = QAction(u"Lune", self.interface.mainWindow())
        QObject.connect(self.import_lune, SIGNAL("triggered()"), lambda: self.gereFonction("import_lune"))

        self.import_soleil = QAction(u"Soleil", self.interface.mainWindow())

        self.import_observation = QAction(u"Observations", self.interface.mainWindow())
        QObject.connect(self.import_observation, SIGNAL("triggered()"), lambda: self.gereFonction("import_observation"))

        iconConfig = QIcon(os.path.dirname(__file__) + "/icons/settings.png")
        self.configure = QAction(iconConfig, u"Configurer le plugin", self.interface.mainWindow())
        QObject.connect(self.configure, SIGNAL("triggered()"), lambda: self.gereFonction("configuration"))

        icon = QIcon(os.path.dirname(__file__) + "/icons/loading.png")
        self.loadData = QAction(icon, u"Charger les données", self.interface.mainWindow())
        QObject.connect(self.loadData, SIGNAL("triggered()"), lambda: self.gereFonction("chargement"))


        iconAPropos = QIcon(os.path.dirname(__file__) + "/icons/ecologism.png")
        self.about = QAction(iconAPropos, u"À propos", self.interface.mainWindow())
        QObject.connect(self.about, SIGNAL("triggered()"), lambda: self.gereFonction("a_propos"))

        iconAide = QIcon(os.path.dirname(__file__) + "/icons/information.png")
        self.help = QAction(iconAide, u"Aide", self.interface.mainWindow())
        QObject.connect(self.help, SIGNAL("triggered()"), lambda: self.gereFonction("aide"))

        #Actions export
        self.export_logger = QAction(u"Export pour logger", self.interface.mainWindow())
        QObject.connect(self.export_logger, SIGNAL("triggered()"), lambda: self.gereFonction("export_logger"))

        self.export_movebank = QAction(u"Export pour Movebank", self.interface.mainWindow())
        QObject.connect(self.export_movebank, SIGNAL("triggered()"), lambda: self.gereFonction("export_movebank"))

        # Gestion sous-menu gestion
        self.gestion.addAction(self.individu_observation)
        self.gestion.addSeparator()
        self.gestion.addAction(self.age)
        self.gestion.addAction(self.cycle_biologique)
        self.gestion.addAction(self.district)
        self.gestion.addAction(self.espece)
        self.gestion.addAction(self.fichier)
        # self.gestion.addAction(self.individu)
        self.gestion.addSeparator()
        self.gestion.addAction(self.type_activite)
        self.gestion.addAction(self.type_maree)
        self.gestion.addAction(self.type_soleil)

        # Gestion sous-menu importation
        self.importation.addAction(self.import_meteo)
        self.importation.addAction(self.import_marees)
        self.importation.addAction(self.import_lune)
        self.importation.addAction(self.import_soleil)
        self.importation.addSeparator()
        self.importation.addAction(self.import_observation)

        # Gestion sous-menu export
        self.export.addAction(self.export_logger)
        self.export.addAction(self.export_movebank)

        # Gestion du menu
        self.menu_geolimi = QMenu(u"GeoLimi")
        self.menu_geolimi.addMenu(self.gestion)
        self.menu_geolimi.addMenu(self.importation)
        self.menu_geolimi.addMenu(self.export)

        self.menu_geolimi.addSeparator()
        self.menu_geolimi.addAction(self.configure)
        self.menu_geolimi.addSeparator()
        self.menu_geolimi.addAction(self.loadData)
        self.menu_geolimi.addSeparator()
        self.menu_geolimi.addAction(self.about)
        self.menu_geolimi.addAction(self.help)

        # Où placer le menu_geolimi
        self.interface.mainWindow().menuBar().insertMenu(self.interface.firstRightStandardMenu().menuAction(),self.menu_geolimi)

    def unload(self):
        self.interface.mainWindow().menuBar().removeAction(self.menu_geolimi.menuAction())

    def controleFenetreOuverte(self, fonctionAOuvrir):
        for fonction, listeInfo in self.dicoFonction.items():
            if fonction != fonctionAOuvrir:
                if listeInfo[0]:
                    listeInfo[1].close()

    def gereFonction(self, laFonction):
        #Fonction gérant les différentes fenêtres à ouvrir selon le choix de l'utilisateur
        if laFonction == "a_propos":
            dlg = AboutDialog()
            result = dlg.exec_()
        elif laFonction == "aide":
            localHelpUrl = (os.path.dirname(__file__) + "/help/index.html")
            localHelpUrl = localHelpUrl.replace("\\", "/")
            QDesktopServices.openUrl(QUrl(localHelpUrl))
        elif laFonction == "chargement":
            dlg = LoadDataDialog()
            result = dlg.exec_()
        elif laFonction == "configuration":
            dlg = ConfigurationDialog()
            result = dlg.exec_()
        elif laFonction == "import_observation":
            connectionParams, couche = self.retrouveParamDbConnexion("observation")
            dlg = ImportObservationDialog()
            result = dlg.exec_()
        elif laFonction == "import_maree":
            dlg = ImportMareeDialog()
            result = dlg.exec_()
        elif laFonction == "import_meteo":
            dlg = ImportMeteoDialog()
            result = dlg.exec_()
        elif laFonction == "import_lune":
            dlg = ImportLuneDialog()
            result = dlg.exec_()
        elif laFonction == "export_logger":
            dlg = ExportLoggerDialog()
            result = dlg.exec_()
        elif laFonction == "export_movebank":
            dlg = ExportMovebankDialog()
            result = dlg.exec_()
        else:
            connectionParams, couche = self.retrouveParamDbConnexion(laFonction)

            if not connectionParams:
                QMessageBox.critical(self.interface.mainWindow(), "Erreur", u"La couche '%s' est absente ..." % (laFonction), QMessageBox.Ok)
            else:
                if self.dicoFonction[laFonction][2] == True:  # fenêtre dockée
                    self.controleFenetreOuverte(laFonction)
                    if not self.dicoFonction[laFonction][0]:
                        self.dicoFonction[laFonction][0] = True
                        if self.dicoFonction[laFonction][1] == None:
                            if laFonction == "individu":
                                connectionParams, couche2 = self.retrouveParamDbConnexion("observation")
                                self.dicoFonction[laFonction][1] = IndividuDialog(self.interface, connectionParams, couche, couche2)
                            #elif laFonction == "observation":
                                #self.dicoFonction[laFonction][1] = ObservationDialog(self.interface, connectionParams, couche)
                            self.dicoFonction[laFonction][1].fermeFenetreFonction.connect(self.surFermetureFenetreFonction)
                        self.interface.addDockWidget(Qt.RightDockWidgetArea, self.dicoFonction[laFonction][1])
                        self.dicoFonction[laFonction][1].show()
                else:
                    db = QSqlDatabase.addDatabase("QPSQL", "db1")
                    db.setDatabaseName(connectionParams["dbname"])
                    db.setUserName(connectionParams["user"])
                    db.setPassword(connectionParams["password"])
                    db.setHostName(connectionParams["host"])
                    db.setPort(int(connectionParams["port"]))
                    dbSchema = connectionParams["schema"]

                    if (not db.open()):
                        QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données ...", QMessageBox.Ok)
                    else:
                        dlg = None

                        if laFonction == "espece":
                            dlg = EspeceDialog(db, dbSchema)
                        # elif laFonction == "espece":
                        #     dlg = EspeceDialog(db, dbSchema)

                        if laFonction == "cycle_biologique":
                            dlg = CycleDialog(db, dbSchema)
                        # elif laFonction == "cycle_biologique":
                        #     dlg = CycleDialog(db, dbSchema)

                        if laFonction == "age":
                            dlg = AgeDialog(db, dbSchema)
                        # elif laFonction == "age":
                        #     dlg = AgeDialog(db, dbSchema)

                        if laFonction == "district_capture":
                            dlg = DistDialog(db, dbSchema)
                        # elif laFonction == "district_capture":
                        #     dlg = AgeDialog(db, dbSchema)

                        if laFonction == "fichier":
                            dlg = FichierDialog(db, dbSchema)
                        # elif laFonction == "fichier":
                        #     dlg = FichierDialog(db, dbSchema)

                        if laFonction == "type_activite":
                            dlg = TypeActiviteDialog(db, dbSchema)
                        # elif laFonction == "fichier":
                        #     dlg = TypeActiviteDialog(db, dbSchema)

                        if laFonction == "type_maree":
                            dlg = MareeDialog(db, dbSchema)
                        # elif laFonction == "fichier":
                        #     dlg = MareeDialog(db, dbSchema)

                        if laFonction == "type_soleil":
                            dlg = SoleilDialog(db, dbSchema)
                        # elif laFonction == "fichier":
                        #     dlg = SoleilDialog(db, dbSchema)

                        result = dlg.exec_()
                        if db.isOpen():
                            db.close()

    def surFermetureFenetreFonction(self, listeFonctionAppelante):
        fonctionAppelante = listeFonctionAppelante[0]
        self.dicoFonction[fonctionAppelante][1].fermeFenetreFonction.disconnect(self.surFermetureFenetreFonction)
        self.dicoFonction[fonctionAppelante][0] = False
        self.dicoFonction[fonctionAppelante][1] = None

    def retrouveInfoNoeud(self, unNoeud, nomTable):
        if unNoeud:
            for enfant in unNoeud.children():
                if isinstance(enfant, QgsLayerTreeGroup):
                    self.retrouveInfoNoeud(enfant, nomTable)
                elif isinstance(enfant, QgsLayerTreeLayer):
                    # if enfant.layerName() == nomTable:
                    if enfant.customProperty("nomOrigine") == nomTable:
                        self.laCouche = enfant


    def retrouveParamDbConnexion(self, nomCouche):
        #Fonction de récupération des paramètres de la base
        ltv = self.interface.layerTreeView()
        currentGroupNode = ltv.currentGroupNode()

        if currentGroupNode.name() == "":
            root = QgsProject.instance().layerTreeRoot()
            if len(root.children()) > 0:
                currentGroupNode = root.children()[0]
            else:
                return None, None
        else:
            if currentGroupNode.name()[0:8] != "Geolimi":
                currentGroupNode = currentGroupNode.parent()

        self.laCouche = None
        self.retrouveInfoNoeud(currentGroupNode, nomCouche)

        if self.laCouche:
            uri = QgsDataSourceURI(self.laCouche.layer().dataProvider().dataSourceUri())
            dbname = uri.database()
            host = uri.host()
            port = uri.port()
            user = uri.username()
            password = uri.password()
            schema = uri.schema()
            table = uri.table()
            connectionParams = {
                'dbname': dbname,
                'host': host,
                'port': port,
                'user': user,
                'password': password,
                'schema': schema,
                'table': table
            }
            return connectionParams, self.laCouche.layer()
        else:
            return None, None
