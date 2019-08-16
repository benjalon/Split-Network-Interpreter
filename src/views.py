# pylint: disable=no-member
# pylint: disable=no-name-in-module
"""Views used in the windowing of the application with PyQt5."""
from os.path import dirname
from PyQt5.QtWidgets import QMainWindow, QTableWidgetItem
from PyQt5.QtWidgets import QListWidgetItem, QTreeWidgetItem
from PyQt5 import uic
from PyQt5.QtGui import QIcon, QColor, QRegExpValidator, QPixmap
from PyQt5 import QtGui
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
        self.split_selection = set()
        self.msa = msa
        self.change_filename(self.controller.process_file_name())
        self.update_table(msa)
        self.update_splits_list()
        self.update_species_list()
        self.split_select_button.clicked.connect(
            self.update_total_split_selection)
        self.splits_list_widget.currentItemChanged.connect(
            self.update_single_split_selection)
        self.update_labels()

    def change_filename(self, filename):
        """Changes the file name at the top of the MSA screen."""
        self.filename_label.setText(filename)

    def update_table(self, processed_msa):
        '''Adds the data to the table'''
        # Create table
        self.table_widget = self.msa_table
        msa = processed_msa.msa()
        self.cols = processed_msa.split_by_column

        self.colour_list = {}
        self.cols_set = set(self.cols)
        self.cols_set.discard(0)
        self.cols_set = list(self.cols_set)
        num_splits = len(self.cols_set)

        colourblind_colours = ['E6194B', '3CB44B', 'FFE119', '4363D8',
                               'F58231', '911EB4', '46F0F0', 'F032E6',
                               'BCF60C', 'FABEBE', '008080', 'E6BEFF',
                               '9A6324', 'FFFAC8', '800000', 'AAFFC3',
                               '808000', 'FFD8B1', '000075', '808080']

        if num_splits <= len(colourblind_colours):
            colours = colourblind_colours
        else:
            colours = colorgen.getColours(num_splits)

        for i, colour in enumerate(colours):
            self.colour_list[i+1] = tuple(int(colour[i:i+2], 16)
                                          for i in (0, 2, 4))

        self.table_widget.setRowCount(len(msa[0]))
        self.table_widget.setVerticalHeaderLabels(processed_msa.species_names)
        self.table_widget.setColumnCount(len(msa))

        self.split_selection = set(self.cols)

        self.original_bg = None

        for i in range(0, len(msa[0])):
            for j in range(0, len(msa)):
                self.table_widget.setColumnWidth(j, 1)
                self.table_widget.setItem(i, j, QTableWidgetItem(msa[j][i]))
                if self.cols[j] > 0 and self.original_bg is None:
                    column = self.table_widget.item(i, j)
                    self.original_bg = column.background()

        self.colour_splits()

    def update_splits_list(self):
        '''Updates the list of splits in the msa view.'''
        for split in self.msa.splits:

            split_parent = QTreeWidgetItem(
                [str(split['split_number'])])

            weight_child = QTreeWidgetItem(
                ["Weight: " + str(split['split_weight'])])
            split_parent.addChild(weight_child)

            half_split_child = QTreeWidgetItem(
                ["Split: " + str(split['split'])])
            split_parent.addChild(half_split_child)

            pixmap = QPixmap(16, 16)
            try:
                ind = self.cols_set.index(split['split_number'])
                colour = self.colour_list[ind+1]
                colour = QColor(colour[0], colour[1], colour[2])
                pixmap.fill(colour)
                split_parent.setIcon(0, QIcon(pixmap))
            except:
                pass

            split_widget = self.splits_list_widget
            split_widget.setColumnCount(1)
            split_widget.setHeaderLabels(["Split"])
            split_widget.addTopLevelItem(split_parent)

    def update_labels(self):
        '''Changes the labels to include specifics about the network.'''
        self.species_label.setText(f"Species ({self.msa.num_species})")
        self.splits_label.setText(f"Splits (Top {self.msa.num_splits})")

    def update_species_list(self):
        '''Updates the list of species in the msa view.'''
        for i, species in enumerate(self.msa.species_names):
            QListWidgetItem(f"{i+1}. {species}", self.species_list_widget)

    def update_single_split_selection(self, split_num=None, add=True):
        '''Updates the list of selected splits.'''
        current = self.splits_list_widget.currentItem()
        split_num = int(current.text(0))

        self.split_selection.clear()
        self.split_selection.add(split_num)

        self.colour_splits()

    def update_total_split_selection(self):
        '''Updates the list of selected splits.'''
        if len(self.split_selection) == 0:
            self.split_selection.clear()
            self.split_selection = set(self.cols)
            self.split_select_button.setText('Deselect All')
        else:
            self.split_selection.clear()
            self.split_select_button.setText('Select All')

        self.colour_splits()

    def colour_splits(self):
        '''Colours the splits based on the selection.'''
        for i in range(0, self.msa.num_species):
            for j in range(0, self.msa.num_columns):

                if self.cols[j] == 101010:
                    self.table_widget.item(i, j).setBackground(
                        QColor(128, 128, 128))
                else:
                    if self.cols[j] > 0 and self.cols[j] in self.split_selection:
                        ind = self.cols_set.index(self.cols[j]) + 1
                        colour = self.colour_list[ind]
                        self.table_widget.item(i, j).setBackground(
                            QColor(colour[0], colour[1], colour[2]))
                    else:
                        self.table_widget.item(i, j).setBackground(
                            self.original_bg)


class SettingsWindow(QMainWindow):
    """SettingsWindow contains functions for the settings.ui with PyQt5"""

    def __init__(self, controller, parent=None):
        super(SettingsWindow, self).__init__(parent)
        file_name = '/UI_Templates/settings.ui'
        current_dir = dirname(__file__)
        file_path = current_dir[:-3] + file_name
        uic.loadUi(file_path, self)
        self.controller = controller

        validator = QRegExpValidator(QRegExp("[0-9]*"), self)
        self.split_number_input.setValidator(validator)
        self.split_number_input.setText("10")

        self.partition_metric_input.addItem("Rand Index")
        self.partition_metric_input.addItem("Jaccard Index")

        self.start_button.clicked.connect(controller.get_settings_values)

    def get_settings_value(self):
        '''Returns a dict with the values of the stettings screen'''
        settings = {}
        settings['metric'] = str(self.partition_metric_input.currentText())
        settings['upper_limit'] = float(self.upper_limit_input.value())

        top_splits = int(self.split_number_input.text())
        if top_splits == 0:
            top_splits = None
        else:
            top_splits = top_splits
        settings['top_splits'] = top_splits

        settings['threading'] = bool(self.multithreading_checkbox.isChecked())
        settings['colourblind'] = bool(self.colourblind_checkbox.isChecked())

        return settings


class LoadingWindow(QMainWindow):
    """LoadingWindow contains functions for the loadingScreen.ui with PyQt5"""

    def __init__(self, controller, parent=None):
        super(LoadingWindow, self).__init__(parent)
        file_name = '/UI_Templates/loading.ui'
        current_dir = dirname(__file__)
        file_path = current_dir[:-3] + file_name
        uic.loadUi(file_path, self)
        self.controller = controller
