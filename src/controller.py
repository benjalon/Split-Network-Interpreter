"""Controller class which coordinates the interaction between the view and
model."""
import sys

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

import views
import file
from msa_processor import MsaProcessor


class Controller():
    """The controller for the application."""

    def __init__(self):
        self.nexus_file_name = ""
        self.app = QApplication(sys.argv)
        self.current_window = views.StartWindow(self)
        self.current_window.show()
        sys.exit(self.app.exec_())
        self.msa = None

    def upload_file(self):
        """Presents file upload window."""
        upload_box = file.FileUpload()
        self.nexus_file_name = upload_box.openFileNameDialog()
        if self.nexus_file_name:
            upload_box.hide()
            self.msa = MsaProcessor(
                self.nexus_file_name, threading=True, top_splits=80)
            self.load_settings_screen()

    def load_msa_screen(self):
        """Loads the msa screen"""
        self.current_window.hide()
        self.current_window = views.MSAWindow(
            self, self.msa, self.current_window)
        self.current_window.showMaximized()

    def load_settings_screen(self):
        '''Loads the settings screen'''
        self.current_window.hide()
        new_window = views.SettingsWindow(self, self.current_window)
        new_window.show()
        #self.current_window = new_window

    def load_loading_screen(self):
        '''Loads the loading screen'''
        self.current_window.hide()
        self.current_window = views.LoadingWindow(self, self.current_window)
        self.current_window.show()
        if self.msa.process_msa():
            self.load_msa_screen()
