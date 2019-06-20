import views
import file
import sys
from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

class Controller(object):        

    #calls the file dialog to select a file
    def uploadFile(self):
        uploadBox = file.FileUpload()
        fileName = uploadBox.openFileNameDialog()
        if fileName:
            MainWindow = QtWidgets.QMainWindow()
            ui = views.Ui_MsaScreen(self)
            ui.setupUi(MainWindow)
            MainWindow.show()
            

    def start(self):
        #self.MainWindow.show()
        print("start")
        app = QtWidgets.QApplication(sys.argv)
        MainWindow = QtWidgets.QMainWindow()
        ui = views.Ui_StartScreen(self)
        ui.setupUi(MainWindow)
        MainWindow.show()
        sys.exit(app.exec_())
        


if __name__ == "__main__":
    controller = Controller()
    controller.start()
