"""Views used in the windowing of the application with PyQt5."""
from os.path import dirname
from PyQt5.QtWidgets import QApplication, QMainWindow, QTableWidgetItem, QListWidgetItem
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QColor, QIntValidator, QRegExpValidator
from PyQt5.QtCore import QRegExp
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


class MSAWindow(QMainWindow):
    """MSAWindow contains functions for the msaView.ui with PyQt5"""

    def __init__(self, controller, msa, parent=None):
        self.controller = controller
        super(MSAWindow, self).__init__(parent)
        file_name = '/UI_Templates/msaView.ui'
        current_dir = dirname(__file__)
        file_path = current_dir[:-3] + file_name
        uic.loadUi(file_path, self)
        self.msa = msa
        self.change_filename(self.controller.process_file_name)
        self.update_table(msa)
        self.update_species_list()

    def change_filename(self, filename):
        """Changes the file name at the top of the MSA screen."""
        self.filename_label.setText(filename)
        self.update_splits_list()

    def update_table(self, processed_msa):
        # Create table
        self.tableWidget = self.msa_table
        #self.tableWidget.horizontalHeader().setStretchLastSection(True)
        msa = processed_msa.msa()
        cols = processed_msa.split_by_column

        colour_list = {}
        cols_set = set(cols)
        cols_set.discard(0)
        cols_set = list(cols_set)
        num_splits = len(cols_set)

        colours = colorgen.getColours(num_splits)
        for i, colour in enumerate(colours):
            colour_list[i+1] = tuple(int(colour[i:i+2], 16) for i in (0, 2, 4))

        self.tableWidget.setRowCount(len(msa[0]))
        self.tableWidget.setVerticalHeaderLabels(processed_msa.species_names)
        self.tableWidget.setColumnCount(len(msa))

        for i in range(0, len(msa[0])):
            for j in range(0, len(msa)):
                self.tableWidget.setColumnWidth(j, 1)
                self.tableWidget.setItem(i, j, QTableWidgetItem(msa[j][i]))
                if (cols[j] > 0):
                    ind = cols_set.index(cols[j]) + 1
                    colour = colour_list[ind]
                    self.tableWidget.item(i, j).setBackground(
                        QColor(colour[0], colour[1], colour[2]))

    def update_splits_list(self, splits="hi"):
        for split in self.msa.splits:
            item = f"Split:{split['split_number']} - Weight {split['split_weight']}"
            QListWidgetItem(item, self.splits_list_widget)

    def update_species_list(self):
        for species in self.msa.species_names:
            QListWidgetItem(species, self.species_list_widget)


class SettingsWindow(QMainWindow):
    """SettingsWindow contains functions for the settings.ui with PyQt5"""

    def __init__(self, controller, parent=None):
        super(SettingsWindow, self).__init__(parent)
        file_name = '/UI_Templates/settings.ui'
        current_dir = dirname(__file__)
        file_path = current_dir[:-3] + file_name
        uic.loadUi(file_path, self)
        self.controller = controller

        int_validator = QIntValidator()
        re = QRegExp("[0-9]*")
        abb = QRegExpValidator(re, self)
        self.split_number_input.setValidator(abb)
        self.upper_limit_input.setValidator(abb)

        self.partition_metric_input.addItem("Rand Index")
        self.partition_metric_input.addItem("Jaccard Index")

        self.start_button.clicked.connect(self._get_settings_value)

    def _get_settings_value(self):
        settings = {}
        settings['metric'] = self.partition_metric_input.currentText()
        print()
        x = 1


class LoadingWindow(QMainWindow):
    """LoadingWindow contains functions for the loadingScreen.ui with PyQt5"""

    def __init__(self, controller, parent=None):
        super(LoadingWindow, self).__init__(parent)
        file_name = '/UI_Templates/loading.ui'
        current_dir = dirname(__file__)
        file_path = current_dir[:-3] + file_name
        uic.loadUi(file_path, self)
        self.controller = controller
