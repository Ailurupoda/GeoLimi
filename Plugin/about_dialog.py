# -*- coding: utf-8 -*-
#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Fenetre à propos

import sys 
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *

from forms.about_form import *

class AboutDialog(QDialog, Ui_about_form):
    #Classe lançant la fenêtre à propos qui renseigne sur le plugin
    def __init__(self, parent=None):
        super(AboutDialog, self).__init__(parent)

        self.setupUi(self)

        self.rejected.connect(self.onReject)
        self.buttonBox.rejected.connect(self.onReject)
        self.buttonBox.accepted.connect(self.onAccept)

    def onAccept(self):
        self.accept()

    def onReject(self):
        self.close()
        
       