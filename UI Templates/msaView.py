# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '.\msaView.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayoutWidget = QtWidgets.QWidget(self.centralwidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(9, 9, 781, 581))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.fileNameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.fileNameLabel.setObjectName("fileNameLabel")
        self.verticalLayout.addWidget(self.fileNameLabel)
        self.msaWidget = QtWidgets.QTableView(self.verticalLayoutWidget)
        self.msaWidget.setObjectName("msaWidget")
        self.verticalLayout.addWidget(self.msaWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.splitsListWidget = QtWidgets.QListView(self.verticalLayoutWidget)
        self.splitsListWidget.setObjectName("splitsListWidget")
        self.horizontalLayout.addWidget(self.splitsListWidget)
        self.specieListWidget = QtWidgets.QListView(self.verticalLayoutWidget)
        self.specieListWidget.setObjectName("specieListWidget")
        self.horizontalLayout.addWidget(self.specieListWidget)
        self.verticalLayout.addLayout(self.horizontalLayout)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.fileNameLabel.setText(_translate("MainWindow", "filename.nex"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

