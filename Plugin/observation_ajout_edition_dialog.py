# -*- coding: utf-8 -*-
import sys 
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.observation_ajout_edition_form import *

class ObservationAjoutEditionDialog(QDialog, Ui_observation_ajout_edition_form):
    #Classe de lancement de la fenêtre d'ajout ou de modification d'une observation
    def __init__(self, db, dbSchema, wind_id, wobs_id, parent=None):
        #Initialisation des champs de la fenêtre
        super(ObservationAjoutEditionDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

        self.wind_id = wind_id
        self.wobs_id = wobs_id

        #Création du model en fonction de la base pour le cycle biologique
        self.modelCycleBiologique = QSqlTableModel(self, self.db)
        wrelation = self.dbSchema + ".cycle_biologique"
        self.modelCycleBiologique.setTable(wrelation)
        self.modelCycleBiologique.setSort(self.modelCycleBiologique.fieldIndex("cycle_libelle"), Qt.AscendingOrder)
        if (not self.modelCycleBiologique.select()):
            QMessageBox.critical(self, u"Remplissage du modèle cycle biologique",
                                 self.modelCycleBiologique.lastError().text(), QMessageBox.Ok)
        self.cmb_obs_cycle_id.setModel(self.modelCycleBiologique)
        self.cmb_obs_cycle_id.setModelColumn(self.modelCycleBiologique.fieldIndex("cycle_libelle"))

        # Création du model en fonction de la base pour le type d'activité
        self.modelTypeActivite = QSqlTableModel(self, self.db)
        wrelation = self.dbSchema + ".type_activite"
        self.modelTypeActivite.setTable(wrelation)
        self.modelTypeActivite.setSort(self.modelTypeActivite.fieldIndex("tyact_nom"), Qt.AscendingOrder)
        if (not self.modelTypeActivite.select()):
            QMessageBox.critical(self, u"Remplissage du modèle type d'activité", self.modelTypeActivite.lastError().text(), QMessageBox.Ok)
        self.cmb_obs_tyact_id.setModel(self.modelTypeActivite)
        self.cmb_obs_tyact_id.setModelColumn(self.modelTypeActivite.fieldIndex("tyact_nom"))

        if wobs_id:
            #Cas de modification d'une observation
            self.setWindowTitle("Geolimi - Observation - Modification")
            #Récupération des informations liées à l'observation
            query = QSqlQuery(self.db)
            wrelation = self.dbSchema + ".observation "
            wrelation += "LEFT Join brut.fichier on obs_fich_id = fich_id LEFT Join brut.meteo on  met_date_time = date_trunc('hour', obs_date_time) LEFT JOIN brut.maree on obs_date_time between mar_date_time_p1 and mar_date_time_p2 LEFT Join brut.type_maree on tymar_id = mar_tymar_id LEFT JOIN brut.lune on lune_date = date_trunc('day', obs_date_time)"
            # query.prepare("SELECT obs_id, obs_date, obs_heure, obs_searching_time, obs_gps_voltage, obs_gps_temperature, obs_verifiee, obs_distance_points, obs_speed, obs_fich_id, obs_cycle_id, obs_ind_id, obs_tyact_id FROM " + wrelation + " WHERE obs_id = ?")

            query.prepare("SELECT obs_id, obs_date, obs_heure, obs_searching_time, 	obs_gps_voltage, obs_gps_temperature, obs_verifiee, obs_distance_points, obs_speed, obs_fich_id, obs_cycle_id, obs_ind_id, obs_tyact_id, fich_chemin, tymar_libelle, mar_coef, mar_marnage,	met_nebulosite,	met_vent, met_directionv, met_temperature, lune_phase FROM "+ wrelation + " WHERE obs_id = ? ")
            query.addBindValue(self.wobs_id)
            if query.exec_():
                #Association des informations récupérées sur les champs adéquats
                if query.next():
                    self.le_obs_id.setText(str(query.value(0)))
                    self.de_obs_date.setDate(QDate(query.value(1)))
                    self.te_obs_heure.setTime(QTime(query.value(2)))
                    if not(query.value(6)):
                        self.chk_obs_verifiee.setChecked(False)
                    else:
                        self.chk_obs_verifiee.setChecked(query.value(6))

                    for i in range(self.modelCycleBiologique.rowCount()):
                        if self.modelCycleBiologique.record(i).value("cycle_id") == query.value(10):
                            self.cmb_obs_cycle_id.setCurrentIndex(i)

                    for i in range(self.modelTypeActivite.rowCount()):
                        if self.modelTypeActivite.record(i).value("tyact_id") == query.value(12):
                            self.cmb_obs_tyact_id.setCurrentIndex(i)

                    if not (query.value(3)):
                        self.sp_obs_searching_time.setValue(0)
                    else:
                        self.sp_obs_searching_time.setValue(query.value(3))

                    if not (query.value(4)):
                        self.sp_obs_gps_voltage.setValue(0)
                    else:
                        self.sp_obs_gps_voltage.setValue(query.value(4))

                    if not (query.value(5)):
                        self.sp_obs_gps_temperature.setValue(0)
                    else:
                        self.sp_obs_gps_temperature.setValue(query.value(5))

                    if not (query.value(7)):
                        self.sp_obs_distance_points.setValue(0)
                    else:
                        self.sp_obs_distance_points.setValue(query.value(7))

                    if not (query.value(8)):
                        self.sp_obs_speed.setValue(0)
                    else:
                        self.sp_obs_speed.setValue(query.value(8))

                    if not (query.value(13)):
                        self.le_fich_chemin.setText("")
                    else:
                        self.le_fich_chemin.setText(query.value(13))

                    if not (query.value(14)):
                        self.lbl_position_maree.setText("")
                    else:
                        self.lbl_position_maree.setText(query.value(14))

                    if not (query.value(15)):
                        self.lbl_coef_mar.setText("")
                    else:
                        self.lbl_coef_mar.setText(str(query.value(15)))

                    if not (query.value(16)):
                        self.lbl_marnage.setText("")
                    else:
                        self.lbl_marnage.setText(str(query.value(16)))

                    if not (query.value(17)):
                        self.lbl_nebu.setText("")
                    else:
                        self.lbl_nebu.setText(str(query.value(17)))

                    if not (query.value(18)):
                        self.lbl_vent.setText("")
                    else:
                        self.lbl_vent.setText(str(query.value(18)))

                    if not (query.value(19)):
                        self.lbl_direction_v.setText("")
                    else:
                        self.lbl_direction_v.setText(str(query.value(19)))

                    if not (query.value(20)):
                        self.lbl_tempe.setText("")
                    else:
                        self.lbl_tempe.setText(str(query.value(20)))

                    if not (query.value(21)):
                        self.lbl_phase_lune.setText("")
                    else:
                        self.lbl_phase_lune.setText(str(query.value(21)))




        else:
            #Cas de l'ajout d'une observation
            self.setWindowTitle("Geolimi - Observation - Ajout")
            self.wrecord_obs = None

        
    def reject(self):
        #Annulation de la modification
        QDialog.reject(self)

    def accept(self):
        #Validation de la modification/Création
        value = self.de_obs_date.date()
        wobs_date = QDate.toString(value, "yyyy/MM/dd")

        value = self.te_obs_heure.time()
        wobs_heure = QTime.toString(value)

        wobs_verifiee = self.chk_obs_verifiee.isChecked()

        wrecordCycleBiologique = self.cmb_obs_cycle_id.model().record(self.cmb_obs_cycle_id.currentIndex())
        wobs_cycle_id = wrecordCycleBiologique.value(0)

        wrecordTypeActivite = self.cmb_obs_tyact_id.model().record(self.cmb_obs_tyact_id.currentIndex())
        wobs_tyact_id = wrecordTypeActivite.value(0)

        wobs_searching_time = self.sp_obs_searching_time.value()
        wobs_gps_voltage = self.sp_obs_gps_voltage.value()
        wobs_gps_temperature = self.sp_obs_gps_temperature.value()
        wobs_distance_points = self.sp_obs_distance_points.value()
        wobs_speed = self.sp_obs_speed.value()

        query = QSqlQuery(self.db)
        wrelation = self.dbSchema + ".observation"
        wchamps = "obs_date, obs_heure, obs_searching_time, obs_gps_voltage, obs_gps_temperature, obs_verifiee, obs_distance_points, obs_speed, obs_fich_id, obs_cycle_id, obs_ind_id, obs_tyact_id"

        if self.wobs_id:
            query.prepare("UPDATE " + wrelation + " SET obs_date = ?, obs_heure = ?, obs_searching_time = ?, obs_gps_voltage = ?, obs_gps_temperature = ?, obs_verifiee = ?, obs_distance_points = ?, obs_speed = ?, obs_cycle_id = ?, obs_ind_id = ?, obs_tyact_id = ? WHERE obs_id = ?")
        else :
            query.prepare("INSERT INTO " + wrelation + "(obs_date, obs_heure, obs_searching_time, obs_gps_voltage, obs_gps_temperature, obs_verifiee, obs_distance_points, obs_speed, obs_cycle_id, obs_ind_id, obs_tyact_id) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)")

        query.addBindValue(wobs_date)
        query.addBindValue(wobs_heure, )
        query.addBindValue(wobs_searching_time)
        query.addBindValue(wobs_gps_voltage)
        query.addBindValue(wobs_gps_temperature)
        query.addBindValue(wobs_verifiee)
        query.addBindValue(wobs_distance_points)
        query.addBindValue(wobs_speed)
        query.addBindValue(wobs_cycle_id)
        query.addBindValue(self.wind_id)
        query.addBindValue(wobs_tyact_id)

        if self.wobs_id:
            query.addBindValue(self.wobs_id)

        if not query.exec_():
            QMessageBox.critical(self, u"Erreur - Création / modification observation", query.lastError().text(), QMessageBox.Ok)
        else:
            QDialog.accept(self)

