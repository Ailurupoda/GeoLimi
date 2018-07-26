# -*- coding: utf-8 -*-
import sys 
import os
import datetime
import psycopg2
import shutil

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from qgis.core import *
from qgis.gui import *

from PyQt4.QtSql import *

from functools import partial

from forms.individu_form import *

from observation_ajout_edition_dialog import *
from ancien_logger_ajout_dialog import *

class IndividuDialog(QDockWidget, Ui_individu_form):
    fermeFenetreFonction = pyqtSignal(list)

    def __init__(self, interface, connectionParams, couche, couche2):
        QWidget.__init__(self)
        self.setupUi(self)
        self.iface = interface
        self.mc = self.iface.mapCanvas()
        self.couche = couche
        self.coucheObservation = couche2

        x = QSettings()
        self.idTempInd = x.value("geolimi/id", 0)
        self.db = None
        self.dbSchema = ""

        self.modelIndividu = None
        self.mapper = None

        self.modelAncienLogger = None
        self.modelObservation = None

        self.dirty_individu = False
        self.dirty_ancien_logger = False
        self.dirty_observation = False

        self.relEspece = None
        self.relAge = None
        self.relDistrict = None
        self.slot_individu_select_changed = None

        self.row_courant = 0
        self.row_count = 0
        self.infoMessage = u"Individu"
        self.etat_courant = 0


        # self.acti_adresse_ind_id = -1
        # self.acti_adresse_voietyp_id = -1

        self.db = QSqlDatabase.addDatabase("QPSQL", "db1")
        self.db.setDatabaseName(connectionParams["dbname"])
        self.db.setUserName(connectionParams["user"])
        self.db.setPassword(connectionParams["password"])
        self.db.setHostName(connectionParams["host"])
        self.dbSchema = connectionParams["schema"]

        if (not self.db.open()):
            self.clearFields()
            self.activeFields(False)
            self.activeButtons(False, False)
            QMessageBox.critical(self, "Erreur", u"Impossible de se connecter à la base de données ...", QMessageBox.Ok)
        else:
            slot = partial(self.individu_select_changed, 2)

            self.chkFiltreIndividu.clicked.connect(self.changeEtatFiltreIndividu)
            # self.btnFiltreCartoManuel.clicked.connect(slot)
            # self.btnFiltreAttributaire.clicked.connect(self.filtreAttributaire)
            # self.btnDeleteFiltrage.clicked.connect(self.actieco_annule_filtrage)

            self.btnCentrer.clicked.connect(self.centreObservation)
            self.btnZoomer.clicked.connect(self.zoomObservation)
            self.btnSelectionner.clicked.connect(self.selectionObservation)
            self.btnZoomerSelectionner.clicked.connect(self.zoomSelectionObservation)

            self.btnAdd.clicked.connect(self.add)

            self.btnCancel.clicked.connect(self.cancel)
            self.btnValidate.clicked.connect(self.validate)

            self.connect(self.btnFirst, SIGNAL("clicked()"), lambda: self.saveRecord("first"))
            self.connect(self.btnPrev, SIGNAL("clicked()"), lambda: self.saveRecord("prev"))
            self.connect(self.btnNext, SIGNAL("clicked()"), lambda: self.saveRecord("next"))
            self.connect(self.btnLast, SIGNAL("clicked()"), lambda: self.saveRecord("last"))

            self.connect(self.btnDelete, SIGNAL("clicked()"), self.rowDelete)

            # self.btnGereIndice.clicked.connect(self.gereIndice)
            # self.btnGereTypeVoie.clicked.connect(self.gereTypeVoie)
            #
            # self.btnGereFiliale.clicked.connect(self.gereFiliale)
            # self.btnAddFiliale.clicked.connect(self.addFiliale)
            # self.btnDeleteFiliale.clicked.connect(self.deleteFiliale)
            #
            # self.btnGereDirigeant.clicked.connect(self.gereDirigeant)
            # self.btnGereFonction.clicked.connect(self.gereFonction)
            # self.btnAddStaff.clicked.connect(self.addStaff)
            # self.btnDeleteStaff.clicked.connect(self.deleteStaff)

            self.setupModel()
            self.connectDirtyFlagSignals_individu(self.dwc_individu)

            self.btnAddObservation.clicked.connect(self.addObservation)
            self.btnDeleteObservation.clicked.connect(self.deleteObservation)
            self.btnEditObservation.clicked.connect(self.editObservation)

            self.btnAddAncienLogger.clicked.connect(self.addAncienLogger)
            self.btnDeleteAncienLogger.clicked.connect(self.deleteAncienLogger)

            self.init_event()

            if  self.idTempInd > 0:
                self.selectObs(couche2)


    def selectObs(self, couche):
        self.mc
        lesObs = couche.getFeatures()
        self.h_list = []
        for uneObs in lesObs:
            if uneObs.attribute("obs_id") > self.idTempInd:
                self.highlight = QgsHighlight(self.mc, uneObs.geometry(), self.couche)
                self.highlight.setColor(QColor('#CCCCCC'))
                self.highlight.setFillColor(QColor('#68F9E5'))
                self.highlight.setWidth(1.5)
                self.h_list.append(self.highlight)
                # self.mc.refresh()



    def changeEtatFiltreIndividu(self):
        if self.chkFiltreIndividu.isChecked():
            record = self.modelIndividu.record(self.row_courant)
            wind_id = int(record.value("ind_id"))
            self.coucheObservation.setSubsetString('"obs_ind_id" = %i' %(wind_id))
        else:
            self.coucheObservation.setSubsetString('')


    def connectDirtyFlagSignals_individu(self, widget):
        if (isinstance(widget, QLineEdit)):
            widget.textEdited.connect(self.setDirtyFlag_individu)
        if (isinstance(widget, QRadioButton)):
            widget.clicked.connect(self.setDirtyFlag_individu)
        if (isinstance(widget, QComboBox)):
            widget.activated.connect(self.setDirtyFlag_individu)
        if (isinstance(widget, QTextEdit)):
            widget.textChanged.connect(self.setDirtyFlag_individu)
        if (isinstance(widget, QSpinBox)):
            widget.valueChanged.connect(self.setDirtyFlag_individu)
        if (isinstance(widget, QCheckBox)):
            if widget.objectName() != "chkFiltreIndividu":
                widget.clicked.connect(self.setDirtyFlag_individu)

        for child in widget.children():
            self.connectDirtyFlagSignals_individu(child)

    def setDirtyFlag_individu(self):
        self.dirty_individu = True

    def setDirtyFlag_ancien_logger(self):
        self.dirty_ancien_logger = True

    def setDirtyFlag_observation(self):
        self.dirty_observation = True

    def init_event(self):
        if self.couche:
            self.couche.removeSelection()
            # self.slot_actieco_select_changed = partial(self.actieco_select_changed, 1)
            # self.couche.selectionChanged.connect(self.slot_actieco_select_changed)
            self.couche.committedAttributeValuesChanges.connect(self.setupModel)
            self.couche.committedFeaturesAdded.connect(self.setupModel)
            self.couche.beforeCommitChanges.connect(self.individu_beforeCommitChanges)
            self.couche.committedFeaturesRemoved.connect(self.setupModel)
            self.couche.editingStopped.connect(self.individu_editingStopped)

    def disconnect_event(self):
        if self.couche:
            # self.couche.selectionChanged.disconnect(self.slot_actieco_select_changed)
            self.couche.committedAttributeValuesChanges.disconnect(self.setupModel)
            self.couche.committedFeaturesAdded.disconnect(self.setupModel)
            self.couche.beforeCommitChanges.disconnect(self.individu_beforeCommitChanges)
            self.couche.committedFeaturesRemoved.disconnect(self.setupModel)
            self.couche.editingStopped.disconnect(self.individu_editingStopped)
            QObject.disconnect(self.mapper, SIGNAL("currentIndexChanged(int)"), self.rowChange)

    def individu_beforeCommitChanges(self):
        if self.couche.editBuffer():
            idsDeleted = self.couche.editBuffer().deletedFeatureIds()
            if len(idsDeleted) > 0:
                individusIdsDeleted = []
                for entite in self.couche.dataProvider().getFeatures(QgsFeatureRequest().setFilterFids(idsDeleted)):
                    individusIdsDeleted.append(entite.attribute("ind_id"))
                self.delete_cascade(None, individusIdsDeleted)

            dicoEntite = self.couche.editBuffer().addedFeatures()
            for id, entite in dicoEntite.items():
                if entite.attribute("ind_esp_id") == None:
                    self.couche.changeAttributeValue(id, entite.fieldNameIndex("ind_esp_id"), 1, 1)
                if entite.attribute("ind_age_id") == None:
                    self.couche.changeAttributeValue(id, entite.fieldNameIndex("ind_age_id"), 1, 1)
                if entite.attribute("ind_distr_id") == None:
                    self.couche.changeAttributeValue(id, entite.fieldNameIndex("ind_distr_id"), 1, 1)

    def individu_editingStopped(self):
        pass

    def individu_select_changed(self, origine):
        # TODO
        pass
        # if self.etat_courant != 10:
        #     if self.couche:
        #         if self.couche.selectedFeatureCount() != 0:
        #             row = self.mapper.currentIndex()
        #             self.wsubmit("actieco_select_changed", row)
        #             self.mapper.setCurrentIndex(row)
        #
        #             self.btnFiltreCartoManuel.setEnabled(True)
        #             if (origine == 1 and self.chkFiltreCartoAuto.isChecked()) or (origine == 2):
        #                 if (self.couche.selectedFeatureCount() >= 1000) and (QGis.QGIS_VERSION_INT < 21203):
        #                     self.couche.setSelectedFeatures([])
        #                     self.iface.messageBar().pushMessage("Erreur",
        #                                                         u"Le nombre d'éléments sélectionnés est trop important ...",
        #                                                         level=QgsMessageBar.CRITICAL, duration=3)
        #                 else:
        #                     self.infoMessage = u"(FILTRAGE EN COURS) - Activité économique"
        #                     wparam = ""
        #                     for feature in self.couche.selectedFeatures():
        #                         # wid = QgsExpression("$id").evaluate(feature)
        #                         wid = feature.attribute("acti_id")
        #                         wparam += str(wid) + ","
        #                     if (wparam != ""):
        #                         wparam = "(" + wparam[0:len(wparam) - 1] + ")"
        #                         if self.modelActiEco:
        #                             self.modelActiEco.setFilter("acti_id in %s" % wparam)
        #                             self.modelActiEco.select()
        #                             if self.dbType == "spatialite":
        #                                 while self.modelActiEco.canFetchMore():
        #                                     self.modelActiEco.fetchMore()
        #                             self.row_count = self.modelActiEco.rowCount()
        #                             self.mapper.toFirst()
        #                             self.btnDeleteFiltrage.setEnabled(True)
        #
        #         else:
        #             self.btnFiltreCartoManuel.setEnabled(False)

    def individu_annule_filtrage(self):
        # TODO
        pass
        # if self.modelActiEco:
        #     row = self.mapper.currentIndex()
        #     self.wsubmit("actieco_annule_filtrage", row)
        #     self.mapper.setCurrentIndex(row)
        #
        #     self.infoMessage = u"Activité économique"
        #     self.modelActiEco.setFilter("")
        #     self.modelActiEco.select()
        #     if self.dbType == "spatialite":
        #         while self.modelActiEco.canFetchMore():
        #             self.modelActiEco.fetchMore()
        #     self.row_count = self.modelActiEco.rowCount()
        #     self.mapper.toFirst()
        #     self.btnDeleteFiltrage.setEnabled(False)

    def delete_cascade(self, layerId=None, deletedFeatureIds=None):
        if self.db:
            rq = QSqlQuery(self.db)
            for id in deletedFeatureIds:
                # suppression des anciens loggers
                rq.clear()
                wrelation = self.dbSchema + ".ancien_logger"
                rq.prepare("DELETE FROM " + wrelation + " WHERE anc_ind_id = ?")
                rq.addBindValue(id)
                if not rq.exec_():
                    QMessageBox.critical(self, "Erreur", u"Impossible de supprimer les anciens loggers de cet individu ...", QMessageBox.Ok)

                # suppression des observations
                rq.clear()
                wrelation = self.dbSchema + ".observation"
                rq.prepare("DELETE FROM " + wrelation + " WHERE obs_ind_id = ?")
                rq.addBindValue(id)
                if not rq.exec_():
                    QMessageBox.critical(self, "Erreur", u"Impossible de supprimer les observations de cet individu ...", QMessageBox.Ok)
            if layerId:
                self.setupModel()
        else:
            QMessageBox.critical(self, "Erreur", u"Impossible de supprimer dans la base de données ...", QMessageBox.Ok)

    def setupModel(self):
        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))

        self.modelIndividu = QSqlRelationalTableModel(self, self.db)

        wrelation = self.dbSchema + ".individu"

        self.modelIndividu.setTable(wrelation)
        self.modelIndividu.setSort(self.modelIndividu.fieldIndex("ind_id"), Qt.AscendingOrder)

        # combo espèce :
        self.ind_esp_id = self.modelIndividu.fieldIndex("ind_esp_id")
        # TODO
        # wrelation = "v_espece"
        wrelation = self.dbSchema + ".espece"
        # self.modelIndividu.setRelation(self.ind_esp_id, QSqlRelation(wrelation, "esp_id", "esp_nom_complet"))
        self.modelIndividu.setRelation(self.ind_esp_id, QSqlRelation(wrelation, "esp_id", "esp_nomfr"))
        self.relEspece = QSqlTableModel(self, self.db)
        self.relEspece.setTable(wrelation)
        self.relEspece.select()

        # combo age :
        self.ind_age_id = self.modelIndividu.fieldIndex("ind_age_id")
        # TODO
        # wrelation = "v_age"
        wrelation = self.dbSchema + ".age"
        self.modelIndividu.setRelation(self.ind_age_id, QSqlRelation(wrelation, "age_id", "age_libelle"))
        self.relAge = QSqlTableModel(self, self.db)
        self.relAge.setTable(wrelation)
        self.relAge.select()

        # combo district :
        self.ind_distr_id = self.modelIndividu.fieldIndex("ind_distr_id")
        # TODO
        # wrelation = "v_district_capture"
        wrelation = self.dbSchema + ".district_capture"
        self.modelIndividu.setRelation(self.ind_distr_id, QSqlRelation(wrelation, "distr_id", "distr_nom"))
        self.relDistrict = QSqlTableModel(self, self.db)
        self.relDistrict.setTable(wrelation)
        self.relDistrict.select()

        if (not self.modelIndividu.select()):
            QMessageBox.critical(self, u"Remplissage du modèle", self.modelIndividu.lastError().text(), QMessageBox.Ok)

        self.row_count = self.modelIndividu.rowCount()

        self.mapper = QDataWidgetMapper(self)
        self.mapper.setSubmitPolicy(QDataWidgetMapper.ManualSubmit)
        self.mapper.setModel(self.modelIndividu)
        self.mapper.setItemDelegate(QSqlRelationalDelegate(self))

        self.mapper.addMapping(self.le_ind_id, self.modelIndividu.fieldIndex("ind_id"))
        self.mapper.addMapping(self.chk_ind_actif, self.modelIndividu.fieldIndex("ind_actif"))
        self.mapper.addMapping(self.le_ind_log, self.modelIndividu.fieldIndex("ind_log"))
        self.mapper.addMapping(self.le_ind_log, self.modelIndividu.fieldIndex("ind_log"))

        # combo espèce
        self.cmb_ind_esp_id.setModel(self.relEspece)
        self.cmb_ind_esp_id.setModelColumn(self.relEspece.fieldIndex("esp_nomfr"))
        self.mapper.addMapping(self.cmb_ind_esp_id, self.ind_esp_id)

        # combo age
        self.cmb_ind_age_id.setModel(self.relAge)
        self.cmb_ind_age_id.setModelColumn(self.relAge.fieldIndex("age_libelle"))
        self.mapper.addMapping(self.cmb_ind_age_id, self.ind_age_id)

        self.mapper.addMapping(self.chk_ind_sexe_m, self.modelIndividu.fieldIndex("ind_sexe_m"))
        self.mapper.addMapping(self.chk_ind_sexe_verifie, self.modelIndividu.fieldIndex("ind_sexe_verifie"))

        # combo district
        self.cmb_ind_distr_id.setModel(self.relDistrict)
        self.cmb_ind_distr_id.setModelColumn(self.relDistrict.fieldIndex("distr_nom"))
        self.mapper.addMapping(self.cmb_ind_distr_id, self.ind_distr_id)

        self.mapper.addMapping(self.de_ind_date_capt, self.modelIndividu.fieldIndex("ind_date_capt"))
        self.mapper.addMapping(self.le_ind_no_bague, self.modelIndividu.fieldIndex("ind_no_bague"))
        self.mapper.addMapping(self.le_ind_code_gauche, self.modelIndividu.fieldIndex("ind_code_gauche"))
        self.mapper.addMapping(self.le_ind_code_droit, self.modelIndividu.fieldIndex("ind_code_droit"))

        # mesures gérées par rowChange
        self.mapper.addMapping(self.le_ind_aile, self.modelIndividu.fieldIndex("ind_aile"))
        self.mapper.addMapping(self.le_ind_bec, self.modelIndividu.fieldIndex("ind_bec"))
        self.mapper.addMapping(self.le_ind_tarse, self.modelIndividu.fieldIndex("ind_tarse"))
        self.mapper.addMapping(self.le_ind_masse, self.modelIndividu.fieldIndex("ind_masse"))

        # observations
        # ------------------------------------------------------------------------------------------------------------------------------
        self.modelObservation = QSqlRelationalTableModel(self, self.db)

        wrelation = self.dbSchema + ".observation"
        self.modelObservation.setTable(wrelation)
        self.modelObservation.setSort(1, Qt.AscendingOrder)

        # cycle biologique
        obs_cycle_id = self.modelObservation.fieldIndex("obs_cycle_id")
        wrelation = self.dbSchema + ".cycle_biologique"
        self.modelObservation.setRelation(obs_cycle_id, QSqlRelation(wrelation, "cycle_id", "cycle_libelle"))
        self.modelCycleBiologique = self.modelObservation.relationModel(obs_cycle_id)
        # self.modelCycleBiologique.setSort(1, Qt.AscendingOrder)
        self.modelCycleBiologique.select()

        # type d'activité
        obs_tyact_id = self.modelObservation.fieldIndex("obs_tyact_id")
        wrelation = self.dbSchema + ".type_activite"
        self.modelObservation.setRelation(obs_tyact_id, QSqlRelation(wrelation, "tyact_id", "tyact_nom"))
        self.modelTypeActivite = self.modelObservation.relationModel(obs_tyact_id)
        # self.modelTypeActivite.setSort(1, Qt.AscendingOrder)
        self.modelTypeActivite.select()

        self.modelObservation.setHeaderData(self.modelObservation.fieldIndex("obs_id"), Qt.Horizontal, u"ID")
        self.modelObservation.setHeaderData(self.modelObservation.fieldIndex("obs_date"), Qt.Horizontal, u"Date")
        self.modelObservation.setHeaderData(self.modelObservation.fieldIndex("obs_heure"), Qt.Horizontal, u"Heure")
        self.modelObservation.setHeaderData(self.modelObservation.fieldIndex("obs_cycle_id"), Qt.Horizontal, u"Cycle biologique")
        self.modelObservation.setHeaderData(self.modelObservation.fieldIndex("obs_tyact_id"), Qt.Horizontal, u"Activité")
        if (not self.modelObservation.select()):
            QMessageBox.critical(self, u"Remplissage du modèle", self.modelObservation.lastError().text(), QMessageBox.Ok)

        # self.modelObservation.setEditStrategy(QSqlTableModel.OnManualSubmit)

        self.tv_observation.setModel(self.modelObservation)
        # self.tv_observation.model().dataChanged.connect(self.setDirtyFlag_observation)
        self.tv_observation.setItemDelegate(ObservationDelegate(self.modelObservation, self))
        self.tv_observation.setSelectionMode(QTableView.SingleSelection)
        self.tv_observation.setSelectionBehavior(QTableView.SelectRows)

        self.tv_observation.setColumnHidden(self.modelObservation.fieldIndex("obs_id"), True)
        self.tv_observation.setColumnHidden(self.modelObservation.fieldIndex("obs_geom"), True)
        self.tv_observation.setColumnHidden(self.modelObservation.fieldIndex("obs_searching_time"), True)
        self.tv_observation.setColumnHidden(self.modelObservation.fieldIndex("obs_gps_voltage"), True)
        self.tv_observation.setColumnHidden(self.modelObservation.fieldIndex("obs_gps_temperature"), True)
        self.tv_observation.setColumnHidden(self.modelObservation.fieldIndex("obs_verifiee"), True)
        self.tv_observation.setColumnHidden(self.modelObservation.fieldIndex("obs_distance_points"), True)
        self.tv_observation.setColumnHidden(self.modelObservation.fieldIndex("obs_speed"), True)
        self.tv_observation.setColumnHidden(self.modelObservation.fieldIndex("obs_fich_id"), True)
        self.tv_observation.setColumnHidden(self.modelObservation.fieldIndex("obs_ind_id"), True)

        # self.tv_observation.resizeColumnsToContents()
        self.tv_observation.horizontalHeader().setStretchLastSection(True)

        self.tv_observation.setItemDelegateForColumn(self.modelObservation.fieldIndex("obs_date"), DateDelegate(self))

        # anciens loggers
        # ------------------------------------------------------------------------------------------------------------------------------
        self.modelAncienLogger = QSqlRelationalTableModel(self, self.db)

        wrelation = self.dbSchema + ".ancien_logger"
        self.modelAncienLogger.setTable(wrelation)
        self.modelAncienLogger.setSort(0, Qt.AscendingOrder)

        self.modelAncienLogger.setHeaderData(self.modelAncienLogger.fieldIndex("anc_log"), Qt.Horizontal, u"CODE")

        if (not self.modelAncienLogger.select()):
            QMessageBox.critical(self, u"Remplissage du modèle", self.modelObservation.lastError().text(), QMessageBox.Ok)

        # self.modelAncienLogger.setEditStrategy(QSqlTableModel.OnManualSubmit)

        self.tv_ancien_logger.setModel(self.modelAncienLogger)
        # self.tv_ancien_logger.model().dataChanged.connect(self.setDirtyFlag_ancien_logger)
        self.tv_ancien_logger.setItemDelegate(AncienLoggerDelegate(self.modelAncienLogger, self))
        self.tv_ancien_logger.setSelectionMode(QTableView.SingleSelection)
        self.tv_ancien_logger.setSelectionBehavior(QTableView.SelectRows)

        self.tv_ancien_logger.setColumnHidden(self.modelAncienLogger.fieldIndex("anc_ind_id"), True)

        # self.tv_ancien_logger.resizeColumnsToContents()
        self.tv_ancien_logger.horizontalHeader().setStretchLastSection(True)

        # ------------------------------------------------------------------------------------------------------------------------------

        QObject.connect(self.mapper, SIGNAL("currentIndexChanged(int)"), self.rowChange)

        if self.modelIndividu.rowCount() == 0:
            self.clearFields()
            self.activeFields(False)
            self.activeButtons(False, True)
        else:
            self.activeFields(True)
            self.activeButtons(True, True)
            self.mapper.toFirst()
        QApplication.restoreOverrideCursor()

    def clearFields(self):
        self.le_ind_id.setText("")
        self.chk_ind_actif.setChecked(False)
        self.le_ind_log.setText("")
        self.cmb_ind_esp_id.setCurrentIndex(0)
        self.cmb_ind_age_id.setCurrentIndex(0)
        self.chk_ind_sexe_m.setChecked(False)
        self.chk_ind_sexe_verifie.setChecked(False)
        self.cmb_ind_distr_id.setCurrentIndex(0)
        # self.de_ind_date_capt.setEnabled(False)

        y = datetime.date.today().year
        m = datetime.date.today().month
        d = datetime.date.today().day
        print(y)

        self.de_ind_date_capt.setDate(QDate(y, m, d))
        self.le_ind_no_bague.setText("")
        self.le_ind_code_gauche.setText("")
        self.le_ind_code_droit.setText("")
        self.le_ind_aile.setText("")
        self.le_ind_bec.setText("")
        self.le_ind_tarse.setText("")
        self.le_ind_masse.setText("")

        if self.modelObservation:
            self.modelObservation.setFilter("obs_id = 0")

        if self.modelAncienLogger:
            self.modelAncienLogger.setFilter("anc_log = ''")

    def activeFields(self, active):
        self.chk_ind_actif.setEnabled(active)
        self.le_ind_log.setEnabled(active)
        self.cmb_ind_esp_id.setEnabled(active)
        self.cmb_ind_age_id.setEnabled(active)
        self.chk_ind_sexe_m.setEnabled(active)
        self.chk_ind_sexe_verifie.setEnabled(active)
        self.cmb_ind_distr_id.setEnabled(active)
        # self.de_ind_date_capt.setEnabled(False)
        self.de_ind_date_capt.setEnabled(active)
        self.le_ind_no_bague.setEnabled(active)
        self.le_ind_code_gauche.setEnabled(active)
        self.le_ind_code_droit.setEnabled(active)
        self.le_ind_aile.setEnabled(active)
        self.le_ind_bec.setEnabled(active)
        self.le_ind_tarse.setEnabled(active)
        self.le_ind_masse.setEnabled(active)

        self.tv_observation.setEnabled(active)
        self.tv_ancien_logger.setEnabled(active)

    def activeButtons(self, active, btnAddEnabled):

        self.chkFiltreIndividu.setEnabled(active)
        # self.btnFiltreCartoManuel.setEnabled(False)
        # self.chkFiltreCartoAuto.setEnabled(active)
        self.btnFiltreAttributaire.setEnabled(active)
        # self.btnDeleteFiltrage.setEnabled(False)
        # self.btnGereIndice.setEnabled(active)
        # self.btnGereTypeVoie.setEnabled(active)
        # self.btnGereFiliale.setEnabled(active)
        # self.btnAddFiliale.setEnabled(active)
        # self.btnDeleteFiliale.setEnabled(active)
        # self.btnGereDirigeant.setEnabled(active)
        # self.btnGereFonction.setEnabled(active)
        # self.btnAddStaff.setEnabled(active)
        # self.btnDeleteStaff.setEnabled(active)
        self.btnFirst.setEnabled(active)
        self.btnPrev.setEnabled(active)
        self.btnNext.setEnabled(active)
        self.btnLast.setEnabled(active)
        self.btnAdd.setEnabled(btnAddEnabled)
        self.btnDelete.setEnabled(active)
        self.btnValidate.setEnabled(False)
        self.btnCancel.setEnabled(False)
        self.btnCentrer.setEnabled(active)
        self.btnZoomer.setEnabled(active)
        self.btnSelectionner.setEnabled(active)
        self.btnZoomerSelectionner.setEnabled(active)

        self.btnAddObservation.setEnabled(active)
        self.btnDeleteObservation.setEnabled(active)
        self.btnEditObservation.setEnabled(active)

        self.btnAddAncienLogger.setEnabled(active)
        self.btnDeleteAncienLogger.setEnabled(active)

    def saveRecord(self, wfrom):
        row = self.mapper.currentIndex()
        self.wsubmit(wfrom, row)

        if wfrom == "first":
            row = 0
        elif wfrom == "prev":
            row = 0 if row <= 1 else row - 1
        elif wfrom == "next":
            row += 1
            if row >= self.modelIndividu.rowCount():
                row = self.modelIndividu.rowCount() - 1
        elif wfrom == "last":
            row = self.modelIndividu.rowCount() - 1

        self.mapper.setCurrentIndex(row)
        if self.row_count == 1:
            self.rowChange(0)

    def wsubmit(self, wfrom, row):
        if wfrom == "saveRecord" or wfrom == "individu_annule_filtrage" or wfrom == "individu_select_changed" or wfrom == "autre":
            self.le_ind_id.setFocus()
        elif wfrom == "onVisibilityChange":
            self.le_ind_log.setFocus()

        if self.dirty_observation:
            self.modelObservation.submitAll()
            self.dirty_observation = False

        if self.dirty_ancien_logger:
            self.modelAncienLogger.submitAll()
            self.dirty_ancien_logger = False

        # individu
        if self.dirty_individu:
            self.mapper.submit()
            self.dirty_individu = False

    def afficheInfoRow(self):
        self.setWindowTitle(self.infoMessage + " (" + str(self.row_courant + 1) + " / " + str(self.row_count) + ")")

    def rowChange(self, row):
        self.row_courant = row
        # boutons de navigation
        self.btnPrev.setEnabled(row > 0)
        self.btnNext.setEnabled(row < self.modelIndividu.rowCount() - 1)
        self.btnFirst.setEnabled(self.modelIndividu.rowCount() != 0)
        self.btnLast.setEnabled(self.modelIndividu.rowCount() != 0)

        record = self.modelIndividu.record(row)

        # gestion des mesures
        wind_aile = record.value(self.modelIndividu.fieldIndex("ind_aile"))
        if wind_aile == None:
            self.le_ind_aile.setText("")
        else:
            self.le_ind_aile.setText(str(wind_aile))

        wind_bec = record.value(self.modelIndividu.fieldIndex("ind_bec"))
        if wind_bec == None:
            self.le_ind_bec.setText("")
        else:
            self.le_ind_bec.setText(str(wind_bec))

        wind_tarse = record.value(self.modelIndividu.fieldIndex("ind_tarse"))
        if wind_tarse == None:
            self.le_ind_tarse.setText("")
        else:
            self.le_ind_tarse.setText(str(wind_tarse))

        wind_masse = record.value(self.modelIndividu.fieldIndex("ind_masse"))
        if wind_masse == None:
            self.le_ind_masse.setText("")
        else:
            self.le_ind_masse.setText(str(wind_masse))

        # gestion des observations
        id = int(record.value("ind_id"))
        self.modelObservation.setFilter("obs_ind_id = %i" % id)

        # gestion des anciens loggers
        self.modelAncienLogger.setFilter("anc_ind_id = %i" % id)

        self.afficheInfoRow()
        if self.chkFiltreIndividu.isChecked():
            record = self.modelIndividu.record(self.row_courant)
            wind_id = int(record.value("ind_id"))
            self.coucheObservation.setSubsetString('"obs_ind_id" = %i' %(wind_id))

    def rowDelete(self):
        if self.mapper:
            row = self.mapper.currentIndex()
            if row >= 0:
                if QMessageBox.question(self, "Suppression", u"Etes-vous certain de vouloir supprimer cet individus ainsi que toutes les informations associées (observations et anciens loggers) ?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
                    record = self.modelIndividu.record(row)
                    wid = int(record.value("ind_id"))
                    wids = []
                    wids.append(wid)
                    self.delete_cascade(None, wids)
                    # suppression de l'individu
                    self.modelIndividu.removeRow(row)
                    self.modelIndividu.submitAll()
                    self.row_count -= 1
                    row -= 1
                    if row >= 0:
                        self.mapper.setCurrentIndex(row)
                    elif self.row_count > 0:
                        row = 0
                        self.mapper.setCurrentIndex(row)
                    else:
                        self.clearFields()
                        self.activeFields(False)
                        self.activeButtons(False, False)
                        self.btnAdd.setEnabled(True)
                        self.setWindowTitle(self.infoMessage)

                    # pour forcer le rafraichissement
                    self.mc.zoomScale(self.mc.scale() - 1)

                    if self.infoMessage[1:9] == "FILTRAGE" and self.row_count == 0:
                        self.individu_annule_filtrage()
                        if self.row_count == 0:
                            self.clearFields()
                            self.activeFields(False)
                            self.activeButtons(False, True)
                        else:
                            self.rowChange(0)

    def centreObservation(self):
        indexObservation = self.tv_observation.currentIndex()
        indexObservationRow = indexObservation.row()

        if indexObservationRow >= 0:
            wrecord_obs = self.modelObservation.record(indexObservationRow)
            wobs_id = int(wrecord_obs.value("obs_id"))
            scale = self.mc.scale()
            uneRequete = QgsFeatureRequest().setFilterExpression('"obs_id" = %i' % (wobs_id))
            lesEntites = self.coucheObservation.getFeatures(uneRequete)
            extent = None
            for x in lesEntites:
                extent = x.geometry().boundingBox()
            if extent:
                if self.mc.hasCrsTransformEnabled():
                    crsDest = self.mc.mapRenderer().destinationCrs()
                    crsSrc = self.coucheObservation.crs()
                    xform = QgsCoordinateTransform(crsSrc, crsDest)
                    extent = xform.transform(extent)
                self.mc.setExtent(extent)
                self.mc.zoomScale(scale)
                self.mc.refresh()

    def zoomObservation(self, selection=False):
        indexObservation = self.tv_observation.currentIndex()
        indexObservationRow = indexObservation.row()

        if indexObservationRow >= 0:
            wrecord_obs = self.modelObservation.record(indexObservationRow)
            wobs_id = int(wrecord_obs.value("obs_id"))

            uneRequete = QgsFeatureRequest().setFilterExpression('"obs_id" = %i' % (wobs_id))
            lesEntites = self.coucheObservation.getFeatures(uneRequete)
            extent = None
            for x in lesEntites:
                extent = x.geometry().buffer(10, -1).boundingBox()  # 10 mètres
            if extent:
                if self.mc.hasCrsTransformEnabled():
                    crsDest = self.mc.mapRenderer().destinationCrs()
                    crsSrc = self.coucheObservation.crs()
                    xform = QgsCoordinateTransform(crsSrc, crsDest)
                    extent = xform.transform(extent)
                self.mc.setExtent(extent)
                self.mc.refresh()
                if selection:
                    self.etat_courant = 10
                    self.coucheObservation.selectByExpression('"obs_id" = %i' % (wobs_id), QgsVectorLayer.SetSelection)
                    self.etat_courant = 0

    def selectionObservation(self):
        indexObservation = self.tv_observation.currentIndex()
        indexObservationRow = indexObservation.row()

        if indexObservationRow >= 0:
            wrecord_obs = self.modelObservation.record(indexObservationRow)
            wobs_id = int(wrecord_obs.value("obs_id"))
            self.etat_courant = 10
            self.coucheObservation.selectByExpression('"obs_id" = %i' % (wobs_id), QgsVectorLayer.SetSelection)
            self.etat_courant = 0

    def zoomSelectionObservation(self):
        self.zoomObservation(True)

    def activeButtonsModif(self, active):
        # self.btnFiltreCartoManuel.setEnabled(not active)
        # self.chkFiltreCartoAuto.setEnabled(not active)
        # self.btnFiltreAttributaire.setEnabled(not active)
        # self.btnDeleteFiltrage.setEnabled(not active)

        self.chkFiltreIndividu.setEnabled(not active)

        self.btnFirst.setEnabled(not active)
        self.btnPrev.setEnabled(not active)
        self.btnNext.setEnabled(not active)
        self.btnLast.setEnabled(not active)
        self.btnAdd.setEnabled(not active)
        self.btnDelete.setEnabled(not active)

        self.btnValidate.setEnabled(active)
        self.btnCancel.setEnabled(active)

        self.btnCentrer.setEnabled(not active)
        self.btnZoomer.setEnabled(not active)
        self.btnSelectionner.setEnabled(not active)
        self.btnZoomerSelectionner.setEnabled(not active)

        self.tv_observation.setEnabled(not active)
        self.btnAddObservation.setEnabled(not active)
        self.btnDeleteObservation.setEnabled(not active)
        self.btnEditObservation.setEnabled(not active)

        self.tv_ancien_logger.setEnabled(not active)
        self.btnAddAncienLogger.setEnabled(not active)
        self.btnDeleteAncienLogger.setEnabled(not active)

    def editObservation(self):
        indexObservation = self.tv_observation.currentIndex()
        if indexObservation.row() >=0:
            self.ajoutEdition(False)

    def addObservation(self):
        self.ajoutEdition(True)

    def ajoutEdition(self, ajout):
        indexObservation = self.tv_observation.currentIndex()
        indexObservationRow = indexObservation.row()

        row = self.mapper.currentIndex()
        self.wsubmit("autre", row)
        self.mapper.setCurrentIndex(row)

        record = self.modelIndividu.record(self.row_courant)
        wind_id = int(record.value("ind_id"))

        wobs_id = None
        if not ajout and indexObservationRow >= 0:
            wrecord_obs = self.modelObservation.record(indexObservationRow)
            wobs_id = int(wrecord_obs.value("obs_id"))

        dialog = ObservationAjoutEditionDialog(self.db, self.dbSchema, wind_id, wobs_id)

        dialog.setWindowModality(Qt.ApplicationModal)
        if dialog.exec_():
            self.modelObservation.setFilter("obs_ind_id = %i" % wind_id)
            # self.tv_observation.resizeColumnsToContents()
            self.tv_observation.horizontalHeader().setStretchLastSection(True)

    def deleteObservation(self):
        index = self.tv_observation.currentIndex()

        row = self.mapper.currentIndex()
        self.wsubmit("deleteObservation", row)
        self.mapper.setCurrentIndex(row)

        if not index.isValid():
            return
        if QMessageBox.question(self, u"Observation", u"Confirmez-vous la suppression de l'observation de cet individu ?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.modelObservation.removeRow(index.row())
            self.modelObservation.submitAll()

    def addAncienLogger(self):
        row = self.mapper.currentIndex()
        self.wsubmit("autre", row)
        self.mapper.setCurrentIndex(row)

        record = self.modelIndividu.record(self.row_courant)
        wind_id = int(record.value("ind_id"))

        dialog = AncienLoggerAjoutDialog(self.db, self.dbSchema, wind_id)
        dialog.setWindowModality(Qt.ApplicationModal)
        if dialog.exec_():
            self.modelAncienLogger.setFilter("anc_ind_id = %i" % wind_id)
            # self.tv_ancien_logger.resizeColumnsToContents()
            self.tv_ancien_logger.horizontalHeader().setStretchLastSection(True)

    def deleteAncienLogger(self):
        index = self.tv_ancien_logger.currentIndex()

        row = self.mapper.currentIndex()
        self.wsubmit("deleteAncienLogger", row)
        self.mapper.setCurrentIndex(row)

        if not index.isValid():
            return
        if QMessageBox.question(self, u"Ancien logger", u"Confirmez-vous la suppression de l'ancien logger de cet individu ?", QMessageBox.Yes | QMessageBox.No) == QMessageBox.Yes:
            self.modelAncienLogger.removeRow(index.row())
            self.modelAncienLogger.submitAll()

    def add(self):
        self.couche.removeSelection()
        # self.couche2.removeSelection()

        self.individu_annule_filtrage()

        self.activeButtonsModif(True)
        self.clearFields()
        self.activeFields(True)

    def add_cancel(self, repositionnement=True):
        self.activeButtonsModif(False)
        # TODO
        # self.btnFiltreCartoManuel.setEnabled(False)
        # self.btnDeleteFiltrage.setEnabled(False)

        self.mapper.revert()

        if self.row_count == 0:
            self.clearFields()
            self.activeFields(False)
            self.activeButtons(False, True)
        else:
            if repositionnement:
                self.rowChange(self.row_courant)
            else:
                self.saveRecord("last")

    def add_validate(self):
        if self.saisie_individu_ok():
            self.dirty_individu = True

            wind_actif = self.chk_ind_actif.isChecked()
            wind_log = self.le_ind_log.text()

            wrecord = self.cmb_ind_esp_id.model().record(self.cmb_ind_esp_id.currentIndex())
            wind_esp_id = int(wrecord.value(0))

            wrecord = self.cmb_ind_age_id.model().record(self.cmb_ind_age_id.currentIndex())
            wind_age_id = int(wrecord.value(0))

            wind_sexe_m = self.chk_ind_sexe_m.isChecked()
            wind_sexe_verifie = self.chk_ind_sexe_verifie.isChecked()

            wrecord = self.cmb_ind_distr_id.model().record(self.cmb_ind_distr_id.currentIndex())
            wind_distr_id = int(wrecord.value(0))

            value = self.de_ind_date_capt.date()
            wind_date_capt = QDate.toString(value, "yyyy/MM/dd")

            wind_no_bague = self.le_ind_no_bague.text()
            wind_code_gauche = self.le_ind_code_gauche.text()
            wind_code_droit = self.le_ind_code_droit.text()

            if self.le_ind_aile.text() == "":
                wind_aile = 0.0
            else:
                wind_aile = float(self.le_ind_aile.text())

            if self.le_ind_bec.text() == "":
                wind_bec = 0.0
            else:
                wind_bec = float(self.le_ind_bec.text())

            if self.le_ind_tarse.text() == "":
                wind_tarse = 0.0
            else:
                wind_tarse = float(self.le_ind_tarse.text())

            if self.le_ind_masse.text() == "":
                wind_masse = 0.0
            else:
                wind_masse = float(self.le_ind_masse.text())

            query = QSqlQuery(self.db)

            wrelation = self.dbSchema + ".individu"
            query.prepare("INSERT INTO " + wrelation + "(ind_sexe_m, ind_aile, ind_bec, ind_tarse, ind_masse, ind_date_capt, ind_no_bague, ind_log, ind_code_droit, ind_code_gauche, ind_esp_id, ind_distr_id, ind_age_id, ind_actif, ind_sexe_verif) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);")

            query.addBindValue(wind_sexe_m)
            print(wind_sexe_m)
            query.addBindValue(wind_aile)
            print(wind_aile)
            query.addBindValue(wind_bec)
            print wind_bec
            query.addBindValue(wind_tarse)
            print wind_tarse
            query.addBindValue(wind_masse)
            print wind_masse
            query.addBindValue(wind_date_capt)
            print wind_date_capt
            query.addBindValue(wind_no_bague)
            print wind_no_bague
            query.addBindValue(wind_log)
            print wind_log
            query.addBindValue(wind_code_droit)
            print wind_code_droit
            query.addBindValue(wind_code_gauche)
            print wind_code_gauche
            query.addBindValue(wind_esp_id)
            print wind_esp_id
            query.addBindValue(wind_distr_id)
            print wind_distr_id
            query.addBindValue(wind_age_id)
            print wind_age_id
            query.addBindValue(wind_actif)
            print wind_actif
            query.addBindValue(wind_sexe_verifie)
            print wind_sexe_verifie

            if not query.exec_():
                QMessageBox.critical(self, u"Erreur - création individu", query.lastError().text(), QMessageBox.Ok)
            else:
                self.row_count += 1
                wind_id = 0
                query = QSqlQuery(self.db)

                wrelation = self.dbSchema + ".individu"
                query.prepare("SELECT ind_id FROM " + wrelation + " ORDER BY ind_id DESC LIMIT 1")
                if query.exec_():
                    if query.next():
                        wind_id = query.value(0)
                        self.le_ind_id.setText(str(wind_id))
                if self.row_count == 1:
                    self.modelIndividu.select()
            self.add_cancel(False)
            # self.couche.triggerRepaint()

    def saisie_individu_ok(self):
        # TODO
        ret = True
        # voir si contrôles de saisie
        return ret

    def cancel(self):
        self.add_cancel()

    def validate(self):
        self.add_validate()

    def filtreAttributaire(self):
        pass
        # row = self.mapper.currentIndex()
        # self.wsubmit("actieco_select_changed", row)
        # self.mapper.setCurrentIndex(row)
        #
        # dialog = InfoPrincipaleFiltrage_dialog(self.db, self.dbType, self.dbSchema, self.modelActiEco)
        # dialog.setWindowModality(Qt.ApplicationModal)
        # if dialog.exec_():
        #     self.row_count = self.modelActiEco.rowCount()
        #     if self.row_count != 0:
        #         self.infoMessage = u"(FILTRAGE EN COURS) - Activité économique"
        #         self.mapper.toFirst()
        #         self.btnDeleteFiltrage.setEnabled(True)

    def gereEspece(self):
        pass

    def gereAge(self):
        pass

    def gereDistrict(self):
        pass

    def gereLogger(self):
        pass

    def closeEvent(self, event):
        self.saveRecord("onVisibilityChange")

        self.disconnect_event()

        self.cmb_ind_esp_id.setModel(None)
        self.cmb_ind_age_id.setModel(None)
        self.cmb_ind_distr_id.setModel(None)
        self.tv_observation.setModel(None)
        self.tv_ancien_logger.setModel(None)
        self.mapper.setModel(None)

        del self.relEspece
        del self.relAge
        del self.relDistrict
        del self.modelObservation
        del self.modelAncienLogger
        del self.modelIndividu

        self.db.close()
        del self.db
        self.db = None
        QSqlDatabase.removeDatabase('db1')

        self.fermeFenetreFonction.emit(["individu"])
        event.accept()

class CheckBoxDelegate(QStyledItemDelegate):
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        return None

    def paint(self, painter, option, index):
        if str(index.data()).lower() == "true":
            checked = True
        else:
            checked = False
        check_box_style_option = QStyleOptionButton()
        if (index.flags() & Qt.ItemIsEditable) > 0:
            check_box_style_option.state |= QStyle.State_Enabled
        else:
            check_box_style_option.state |= QStyle.State_ReadOnly
        if checked:
            check_box_style_option.state |= QStyle.State_On
        else:
            check_box_style_option.state |= QStyle.State_Off
        check_box_style_option.rect = self.getCheckBoxRect(option)
        check_box_style_option.state |= QStyle.State_Enabled
        QApplication.style().drawControl(QStyle.CE_CheckBox, check_box_style_option, painter)

    def editorEvent(self, event, model, option, index):
        # Do not change the checkbox-state
        if event.type() == QEvent.MouseButtonPress:
            return False
        if event.type() == QEvent.MouseButtonRelease or event.type() == QEvent.MouseButtonDblClick:
            if event.button() != Qt.LeftButton or not self.getCheckBoxRect(option).contains(event.pos()):
                return False
            if event.type() == QEvent.MouseButtonDblClick:
                return True
        elif event.type() == QEvent.KeyPress:
            if event.key() != Qt.Key_Space and event.key() != Qt.Key_Select:
                return False
            else:
                return False
        # Change the checkbox-state
        self.setModelData(None, model, index)
        return True

    def setModelData(self, editor, model, index):
        newValue = not index.data()
        model.setData(index, newValue, Qt.EditRole)

    def getCheckBoxRect(self, option):
        check_box_style_option = QStyleOptionButton()
        check_box_rect = QApplication.style().subElementRect(QStyle.SE_CheckBoxIndicator, check_box_style_option, None)
        check_box_point = QPoint(option.rect.x() +
                                 option.rect.width() / 2 -
                                 check_box_rect.width() / 2,
                                 option.rect.y() +
                                 option.rect.height() / 2 -
                                 check_box_rect.height() / 2)
        return QRect(check_box_point, check_box_rect.size())

class DateDelegate(QItemDelegate):
    def __init__(self, parent):
        QItemDelegate.__init__(self, parent)

    def createEditor(self, parent, option, index):
        self.dateEdit = QDateTimeEdit(parent)
        self.dateEdit.setCalendarPopup(True)
        self.dateEdit.setDisplayFormat("dd-MM-yyyy")
        return self.dateEdit

    def paint(self, painter, option, index):
        painter.save()
        self.drawBackground(painter, option, index)
        wdate = index.model().data(index)
        if type(wdate) is QDate:
            dateStr = QDate.toString(wdate, "yyyy-MM-dd")
        else:
            dateStr = wdate
        date = QDate.fromString(dateStr, "yyyy-MM-dd")
        value_str = QDate.toString(date, "dd-MM-yyyy")

        rect = option.rect
        painter.drawText(rect.x() + 2, rect.y() + 2, rect.width() - 4, rect.height() - 4,
                         Qt.AlignVCenter | Qt.AlignHCenter, value_str)
        painter.restore()

    def setModelData(self, editor, model, index):
        value = self.dateEdit.date()
        strDate = QDate.toString(value, "yyyy-MM-dd")
        model.setData(index, strDate, Qt.EditRole)

class ObservationDelegate(QSqlRelationalDelegate):
    def __init__(self, model=None, parent=None):
        super(ObservationDelegate, self).__init__(parent)
        self.model = model

    def paint(self, painter, option, index):
        myoption = QStyleOptionViewItem(option)

        # if index.column() == 7 or index.column() == 8 or index.column() == 9:
        #     valeur = str(index.model().data(index))
        #     painter.drawText(option.rect, Qt.AlignCenter, valeur)
        # else:
        #     QSqlRelationalDelegate.paint(self, painter, myoption, index)

        QSqlRelationalDelegate.paint(self, painter, myoption, index)

    def createEditor(self, parent, option, index):
        return QSqlRelationalDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        QSqlRelationalDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        QSqlRelationalDelegate.setModelData(self, editor, model, index)

class AncienLoggerDelegate(QSqlRelationalDelegate):
    def __init__(self, model=None, parent=None):
        super(AncienLoggerDelegate, self).__init__(parent)
        self.model = model

    def paint(self, painter, option, index):
        myoption = QStyleOptionViewItem(option)

        # if index.column() == 7 or index.column() == 8 or index.column() == 9:
        #     valeur = str(index.model().data(index))
        #     painter.drawText(option.rect, Qt.AlignCenter, valeur)
        # else:
        #     QSqlRelationalDelegate.paint(self, painter, myoption, index)

        QSqlRelationalDelegate.paint(self, painter, myoption, index)

    def createEditor(self, parent, option, index):
        return QSqlRelationalDelegate.createEditor(self, parent, option, index)

    def setEditorData(self, editor, index):
        QSqlRelationalDelegate.setEditorData(self, editor, index)

    def setModelData(self, editor, model, index):
        QSqlRelationalDelegate.setModelData(self, editor, model, index)