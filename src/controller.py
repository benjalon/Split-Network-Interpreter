import views
import file
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class Controller():     
    """The controller for the application."""  
    main = None
    app = None

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
            #do something with msa
            self.load_msa_screen()

    def load_msa_screen(self):
        """Loads the msa screen"""
        self.main.hide()
        msa_screen = views.MSAWindow(self, self.main)
        msa_screen.show()
