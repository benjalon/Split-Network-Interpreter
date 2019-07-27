"""Controller class which coordinates the interaction between the view and model."""
import views
import file
import sys
from msa_processor import MsaProcessor
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot


class Controller():
    """The controller for the application."""

    def __init__(self):
        self.process_file_name = ""
        self.app = QApplication(sys.argv)
        self.main = views.StartWindow(self)
        self.main.show()
        sys.exit(self.app.exec_())

    def upload_file(self):
        """Presents file upload window."""
        upload_box = file.FileUpload()
        self.process_file_name = upload_box.openFileNameDialog()
        if self.process_file_name:
            upload_box.hide()
            msa = MsaProcessor(self.process_file_name, 10)
            self.load_msa_screen(msa)

    def load_msa_screen(self, msa):
        """Loads the msa screen"""
        self.main.hide()
        msa_screen = views.MSAWindow(self, msa, self.main)
        msa_screen.show()
