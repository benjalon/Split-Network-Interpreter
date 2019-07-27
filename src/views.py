"""Views used in the windowing of the application with PyQt5."""
from os.path import dirname
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QColor
import partitionGetter
import colorgen


class StartWindow(QMainWindow):
    """StartWindow contains functions for the startScreen.ui with PyQt5"""

    def __init__(self, controller):
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

    def __init__(self, controller, msa, parent=None):
        self.controller = controller
        super(MSAWindow, self).__init__(parent)
        file_name = '/UI_Templates/msaView.ui'
        current_dir = dirname(__file__)
        file_path = current_dir[:-3] + file_name
        uic.loadUi(file_path, self)
        self.change_filename(self.controller.process_file_name)
        self.update_table(msa)

    def open_other_form(self):
        """Some text"""
        self.parent().show()
        self.close()

    def change_filename(self, filename):
        """Changes the file name at the top of the MSA screen."""
        self.fileNameLabel.setText(filename)

    def update_table(self, msa):
        # Create table
        self.tableWidget = self.msaWidget
        msa = msa.get_msa
        cols = msa.get_splits_per_column()
        n = arr["n"]

        colour_list = {}
        colours = colorgen.getColours(len(arr["splits"]))
        for i, colour in enumerate(colours):
            colour_list[i+1] = tuple(int(colour[i:i+2], 16) for i in (0, 2, 4))

        self.tableWidget.setRowCount(len(msa[0]))
        self.tableWidget.setVerticalHeaderLabels(n.taxa.taxa)
        self.tableWidget.setColumnCount(len(msa))

        for i in range(0, len(msa[0])):
            for j in range(0, len(msa)):
                self.tableWidget.setColumnWidth(j, 1)
                self.tableWidget.setItem(i, j, QTableWidgetItem(msa[j][i]))
                if (cols[j] > 0):
                    colour = colour_list[cols[j]]
                    self.tableWidget.item(i, j).setBackground(
                        QColor(colour[0], colour[1], colour[2]))


