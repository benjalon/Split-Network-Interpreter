"""Views used in the windowing of the application with PyQt5."""
from os.path import dirname
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import uic

class StartWindow(QMainWindow):
    """StartWindow contains functions for the startScreen.ui with PyQt5"""

    def __init__(self,controller):
        super(StartWindow, self).__init__()
        file_name = '/UI_Templates/startScreen.ui'
        current_dir = dirname(__file__)
        file_path = current_dir[:-3] + file_name
        uic.loadUi(file_path, self)
        self.uploadButton.clicked.connect(controller.upload_file)

    def open_other_form(self):
        """Opens the other window"""
        self.hide()
        otherview = MSAWindow(self)
        otherview.show()

class MSAWindow(QMainWindow):
    """MSAWindow contains functions for the msaView.ui with PyQt5"""

    def __init__(self, controller, parent=None):
        self.controller = controller
        super(MSAWindow, self).__init__(parent)
        file_name = '/UI_Templates/msaView.ui'
        current_dir = dirname(__file__)
        file_path = current_dir[:-3] + file_name
        uic.loadUi(file_path, self)
        self.change_filename(self.controller.process_file_name)

    def open_other_form(self):
        """Some text"""
        self.parent().show()
        self.close()

    def change_filename(self, filename):
        """Changes the file name at the top of the MSA screen."""
        self.fileNameLabel.setText(filename)


