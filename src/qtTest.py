import sys
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QAction, QTableWidget, QTableWidgetItem, QVBoxLayout
from PyQt5.QtGui import QIcon, QColor
from PyQt5.QtCore import pyqtSlot
import partitionGetter
import colorgen


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 table - pythonspot.com'
        self.left = 0
        self.top = 0
        self.width = 300
        self.height = 200
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.layout = QVBoxLayout()
        self.layout.addWidget(self.tableWidget)
        self.setLayout(self.layout)

        # Show widget
        self.show()

    def createTable(self):
        # Create table
        self.tableWidget = QTableWidget()
        #arr = partitionGetter.runPG("./beesProcessed.nex")
        msa = arr["msa"]
        cols = arr["colSplit"]
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

        self.tableWidget.move(0, 0)
        # works to change colour
        # self.tableWidget.item(0,0).setBackground(QColor(255,0,0))
        # table selection change
        self.tableWidget.doubleClicked.connect(self.on_click)

    @pyqtSlot()
    def on_click(self):
        print("\n")
        for currentQTableWidgetItem in self.tableWidget.selectedItems():
            print(currentQTableWidgetItem.row(),
                  currentQTableWidgetItem.column(),
                  currentQTableWidgetItem.text())


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
