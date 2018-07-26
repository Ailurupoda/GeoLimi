# -*- coding: utf-8 -*-
import sys 
import os

from PyQt4.QtCore import *
from PyQt4.QtGui import *
from PyQt4.QtSql import *

from forms.ancien_logger_ajout_form import *

class AncienLoggerAjoutDialog(QDialog, Ui_ancien_logger_ajout_form):
    #Fenêtre d'ajout d'un ancien logger à un individu
    def __init__(self, db, dbSchema, wind_id, parent=None):
        super(AncienLoggerAjoutDialog, self).__init__(parent)
        self.db = db
        self.dbSchema = dbSchema
        self.setupUi(self)
        self.btnBox.accepted.connect(self.accept)
        self.btnBox.rejected.connect(self.reject)

        self.wind_id = wind_id

    def reject(self):
        QDialog.reject(self)

    def accept(self):
        wle_anc_log = self.le_anc_log.text()

        query = QSqlQuery(self.db)
        wrelation = self.dbSchema + ".ancien_logger"

        query.prepare("INSERT INTO " + wrelation + " (anc_log, anc_ind_id) VALUES (?, ?);")
        query.addBindValue(wle_anc_log)
        query.addBindValue(self.wind_id)

        if not query.exec_():
            QMessageBox.critical(self, u"Erreur - Ajout ancien logger", query.lastError().text(), QMessageBox.Ok)
        else:
            QDialog.accept(self)

