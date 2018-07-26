# -*- coding: utf-8 -*-

#Antoine Blain, Corentin Falcone, Florent Grasland - Plugin GeoLimi
#Projet Tuteuré LUP SIG 2018
#Gestion de données tracking limicoles
#Lancement du plugin

def classFactory(iface):
    #Lancement du plugin dans QGIS
    #Première action effectué par QGIS qui fait appel à geolimi_plgin.py
    from geolimi_plugin import Geolimi
    return Geolimi(iface)