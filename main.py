import os
import sys
from PyQt5.QtWidgets import (QMainWindow, QApplication, QWidget, QAction, 
                            QTableWidget, QTableWidgetItem, QGridLayout, QVBoxLayout, QHBoxLayout,
                            QLineEdit, QLabel, QPushButton)
from PyQt5.QtGui import QPalette, QColor, QIcon
from PyQt5.QtCore import Qt, QTimer, pyqtSlot

import db_conn
import basic
from threading import Thread, Event

event = Event()
t2 = Thread(target=basic.catchData, args=(event, ))

class App(QWidget):
    filterV = {
        'lastmin':'10',
        'lastmax':'',
        'volumemin':'250000',
        'volumemax':'',
        'openinterestmin':'1000',
        'openinterestmax':'',
        'optionvolumemin':'1800',
        'optionvolumemax':'',
        'dtemin':'0',
        'dtemax':'720',
        'optLastmin':'0.01',
        'optLastmax':'100',
        'optDeltamin':'0.42',
        'optDeltamax':'2.00'
    }
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        # self.setGeometry(self.left, self.top, self.width, self.height)
        self.createTable()

        # Add box layout, add table to box layout and add box layout to widget
        self.mainLayout = QGridLayout()
        self.createFilter()
        self.mainLayout.addWidget(self.tableWidget, 8, 0, 1, 16)
        self.setLayout(self.mainLayout) 

        self.resize(1200, 800)
        self.setWindowTitle("Option Hacker")
        # Show widget
        self.show()
    
    def createFilter(self):
        lastLabel = QLabel("Stock Last")
        lastLabel.setStyleSheet("font-size: 16px;")
        lastMinEdit = QLineEdit('10')
        lastMinEdit.setFixedHeight(32)
        lastMinEdit.setStyleSheet("font-size: 18px;")
        lastMinEdit.editingFinished.connect(lambda: self.changeFilterMeta(lastMinEdit.text(), 'lastmin'))
        minLastLabel = QLabel("Min:")
        minLastLabel.setStyleSheet("font-size: 16px;")
        minLastLabel.setBuddy(lastMinEdit)
        lastMaxEdit = QLineEdit('')
        lastMaxEdit.setFixedHeight(32)
        lastMaxEdit.setStyleSheet("font-size: 18px;")
        lastMaxEdit.editingFinished.connect(lambda: self.changeFilterMeta(lastMaxEdit.text(), 'lastmax'))
        maxLastLabel = QLabel("Max:")
        maxLastLabel.setStyleSheet("font-size: 16px;")
        maxLastLabel.setBuddy(lastMaxEdit)
        self.mainLayout.addWidget(lastLabel, 0, 3, 1, 2)
        self.mainLayout.addWidget(minLastLabel, 0, 5, 1, 1)
        self.mainLayout.addWidget(lastMinEdit, 0, 6, 1, 2)
        self.mainLayout.addWidget(maxLastLabel, 0, 8, 1, 1)
        self.mainLayout.addWidget(lastMaxEdit, 0, 9, 1, 2)

        volumeLabel = QLabel("Stock Volume")
        volumeLabel.setStyleSheet("font-size: 16px;")
        volumeMinEdit = QLineEdit('250000')
        volumeMinEdit.setFixedHeight(32)
        volumeMinEdit.setStyleSheet("font-size: 18px;")
        volumeMinEdit.editingFinished.connect(lambda: self.changeFilterMeta(volumeMinEdit.text(), 'volumemin'))
        minVolumeLabel = QLabel("Min:")
        minVolumeLabel.setStyleSheet("font-size: 16px;")
        minVolumeLabel.setBuddy(volumeMinEdit)
        volumeMaxEdit = QLineEdit('')
        volumeMaxEdit.setFixedHeight(32)
        volumeMaxEdit.setStyleSheet("font-size: 18px;")
        volumeMaxEdit.editingFinished.connect(lambda: self.changeFilterMeta(volumeMaxEdit.text(), 'volumemax'))
        maxVolumeLabel = QLabel("Max:")
        maxVolumeLabel.setStyleSheet("font-size: 16px;")
        maxVolumeLabel.setBuddy(volumeMaxEdit)
        self.mainLayout.addWidget(volumeLabel, 1, 3, 1, 2)
        self.mainLayout.addWidget(minVolumeLabel, 1, 5, 1, 1)
        self.mainLayout.addWidget(volumeMinEdit, 1, 6, 1, 2)
        self.mainLayout.addWidget(maxVolumeLabel, 1, 8, 1, 1)
        self.mainLayout.addWidget(volumeMaxEdit, 1, 9, 1, 2)

        openInterestLabel = QLabel("Option Open Interest")
        openInterestLabel.setStyleSheet("font-size: 16px;")
        openInterestMinEdit = QLineEdit('1000')
        openInterestMinEdit.setFixedHeight(32)
        openInterestMinEdit.setStyleSheet("font-size: 18px;")
        openInterestMinEdit.editingFinished.connect(lambda: self.changeFilterMeta(openInterestMinEdit.text(), 'openinterestmin'))
        minOpenInterestLabel = QLabel("Min:")
        minOpenInterestLabel.setStyleSheet("font-size: 16px;")
        minOpenInterestLabel.setBuddy(openInterestMinEdit)
        openInterestMaxEdit = QLineEdit('')
        openInterestMaxEdit.setFixedHeight(32)
        openInterestMaxEdit.setStyleSheet("font-size: 18px;")
        openInterestMaxEdit.editingFinished.connect(lambda: self.changeFilterMeta(openInterestMaxEdit.text(), 'openinterestmax'))
        maxOpenInterestLabel = QLabel("Max:")
        maxOpenInterestLabel.setStyleSheet("font-size: 16px;")
        maxOpenInterestLabel.setBuddy(openInterestMaxEdit)
        self.mainLayout.addWidget(openInterestLabel, 2, 3, 1, 2)
        self.mainLayout.addWidget(minOpenInterestLabel, 2, 5, 1, 1)
        self.mainLayout.addWidget(openInterestMinEdit, 2, 6, 1, 2)
        self.mainLayout.addWidget(maxOpenInterestLabel, 2, 8, 1, 1)
        self.mainLayout.addWidget(openInterestMaxEdit, 2, 9, 1, 2)

        optionvolumeLabel = QLabel("Option Volume")
        optionvolumeLabel.setStyleSheet("font-size: 16px;")
        optionvolumeMinEdit = QLineEdit('1800')
        optionvolumeMinEdit.setFixedHeight(32)
        optionvolumeMinEdit.setStyleSheet("font-size: 18px;")
        optionvolumeMinEdit.editingFinished.connect(lambda: self.changeFilterMeta(optionvolumeMinEdit.text(), 'optionvolumemin'))
        minoptionVolumeLabel = QLabel("Min:")
        minoptionVolumeLabel.setStyleSheet("font-size: 16px;")
        minoptionVolumeLabel.setBuddy(optionvolumeMinEdit)
        optionvolumeMaxEdit = QLineEdit('')
        optionvolumeMaxEdit.setFixedHeight(32)
        optionvolumeMaxEdit.setStyleSheet("font-size: 18px;")
        optionvolumeMaxEdit.editingFinished.connect(lambda: self.changeFilterMeta(optionvolumeMaxEdit.text(), 'optionvolumemax'))
        maxoptionVolumeLabel = QLabel("Max:")
        maxoptionVolumeLabel.setStyleSheet("font-size: 16px;")
        maxoptionVolumeLabel.setBuddy(optionvolumeMaxEdit)
        self.mainLayout.addWidget(optionvolumeLabel, 3, 3, 1, 2)
        self.mainLayout.addWidget(minoptionVolumeLabel, 3, 5, 1, 1)
        self.mainLayout.addWidget(optionvolumeMinEdit, 3, 6, 1, 2)
        self.mainLayout.addWidget(maxoptionVolumeLabel, 3, 8, 1, 1)
        self.mainLayout.addWidget(optionvolumeMaxEdit, 3, 9, 1, 2)

        dteLabel = QLabel("Option Days to Expire")
        dteLabel.setStyleSheet("font-size: 16px;")
        dteMinEdit = QLineEdit('0')
        dteMinEdit.setFixedHeight(32)
        dteMinEdit.setStyleSheet("font-size: 18px;")
        dteMinEdit.editingFinished.connect(lambda: self.changeFilterMeta(dteMinEdit.text(), 'dtemin'))
        dteMinLabel = QLabel("Min:")
        dteMinLabel.setStyleSheet("font-size: 16px;")
        dteMinLabel.setBuddy(dteMinEdit)
        dteMaxEdit = QLineEdit('720')
        dteMaxEdit.setFixedHeight(32)
        dteMaxEdit.setStyleSheet("font-size: 18px;")
        dteMaxEdit.editingFinished.connect(lambda: self.changeFilterMeta(dteMaxEdit.text(), 'dtemax'))
        dteMaxLabel = QLabel("Max:")
        dteMaxLabel.setStyleSheet("font-size: 16px;")
        dteMaxLabel.setBuddy(dteMaxEdit)
        self.mainLayout.addWidget(dteLabel, 4, 3, 1, 2)
        self.mainLayout.addWidget(dteMinLabel, 4, 5, 1, 1)
        self.mainLayout.addWidget(dteMinEdit, 4, 6, 1, 2)
        self.mainLayout.addWidget(dteMaxLabel, 4, 8, 1, 1)
        self.mainLayout.addWidget(dteMaxEdit, 4, 9, 1, 2)

        optLastLabel = QLabel("Option Last")
        optLastLabel.setStyleSheet("font-size: 16px;")
        optLastMinEdit = QLineEdit('0.01')
        optLastMinEdit.setFixedHeight(32)
        optLastMinEdit.setStyleSheet("font-size: 18px;")
        optLastMinEdit.editingFinished.connect(lambda: self.changeFilterMeta(optLastMinEdit.text(), 'optLastmin'))
        optLastMinLabel = QLabel("Min:")
        optLastMinLabel.setStyleSheet("font-size: 16px;")
        optLastMinLabel.setBuddy(optLastMinEdit)
        optLastMaxEdit = QLineEdit('100')
        optLastMaxEdit.setFixedHeight(32)
        optLastMaxEdit.setStyleSheet("font-size: 18px;")
        optLastMaxEdit.editingFinished.connect(lambda: self.changeFilterMeta(optLastMaxEdit.text(), 'optLastmax'))
        optLastMaxLabel = QLabel("Max:")
        optLastMaxLabel.setStyleSheet("font-size: 16px;")
        optLastMaxLabel.setBuddy(optLastMaxEdit)
        self.mainLayout.addWidget(optLastLabel, 5, 3, 1, 2)
        self.mainLayout.addWidget(optLastMinLabel, 5, 5, 1, 1)
        self.mainLayout.addWidget(optLastMinEdit, 5, 6, 1, 2)
        self.mainLayout.addWidget(optLastMaxLabel, 5, 8, 1, 1)
        self.mainLayout.addWidget(optLastMaxEdit, 5, 9, 1, 2)

        optDeltaLabel = QLabel("Option Delta")
        optDeltaLabel.setStyleSheet("font-size: 16px;")
        optDeltaMinEdit = QLineEdit('0.42')
        optDeltaMinEdit.setFixedHeight(32)
        optDeltaMinEdit.setStyleSheet("font-size: 18px;")
        optDeltaMinEdit.editingFinished.connect(lambda: self.changeFilterMeta(optDeltaMinEdit.text(), 'optDeltamin'))
        optDeltaMinLabel = QLabel("Min:")
        optDeltaMinLabel.setStyleSheet("font-size: 16px;")
        optDeltaMinLabel.setBuddy(optDeltaMinEdit)
        optDeltaMaxEdit = QLineEdit('2.00')
        optDeltaMaxEdit.setFixedHeight(32)
        optDeltaMaxEdit.setStyleSheet("font-size: 18px;")
        optDeltaMaxEdit.editingFinished.connect(lambda: self.changeFilterMeta(optDeltaMaxEdit.text(), 'optDeltamax'))
        optDeltaMaxLabel = QLabel("Max:")
        optDeltaMaxLabel.setStyleSheet("font-size: 16px;")
        optDeltaMaxLabel.setBuddy(optDeltaMaxEdit)
        self.mainLayout.addWidget(optDeltaLabel, 6, 3, 1, 2)
        self.mainLayout.addWidget(optDeltaMinLabel, 6, 5, 1, 1)
        self.mainLayout.addWidget(optDeltaMinEdit, 6, 6, 1, 2)
        self.mainLayout.addWidget(optDeltaMaxLabel, 6, 8, 1, 1)
        self.mainLayout.addWidget(optDeltaMaxEdit, 6, 9, 1, 2)

        scanBtn = QPushButton("&Scan")
        scanBtn.setFixedHeight(32)
        scanBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color='#075F12'))
        scanBtn.clicked.connect(lambda: self.scan())
        exportBtn = QPushButton("&Export")
        exportBtn.setFixedHeight(32)
        exportBtn.setStyleSheet("background-color : {color}; color: #FFF; font-weight: bold; font-size: 18px;".format(color='#075F12'))
        exportBtn.clicked.connect(lambda: self.export())
        self.mainLayout.addWidget(scanBtn, 6, 11, 1, 1)
        self.mainLayout.addWidget(exportBtn, 6, 12, 1, 1)

    def createTable(self):
        self.tableWidget = QTableWidget()
        self.tableWidget.setColumnCount(9)
        self.tableWidget.setHorizontalHeaderLabels(["Symbol", "Description", "Last", "Net Change", "Bid", "Ask", "Volume", "Open Interest", "P/C Ratio"])

    def changeFilterMeta(self, data, col):
        self.filterV[col] = data
        print(self.filterV)
    
    def scan(self):
        while self.tableWidget.rowCount() > 0:
            self.tableWidget.removeRow(0)
        data = db_conn.scanData(self.filterV)
        self.tableWidget.setRowCount(len(data))
        index = 0
        for row in data:
            self.tableWidget.setItem(index, 0, QTableWidgetItem(row['symbol']))
            self.tableWidget.setItem(index, 1, QTableWidgetItem(row['description']))
            self.tableWidget.setItem(index, 2, QTableWidgetItem(row['last']))
            self.tableWidget.setItem(index, 3, QTableWidgetItem(row['netchg']))
            self.tableWidget.setItem(index, 4, QTableWidgetItem(row['bid']))
            self.tableWidget.setItem(index, 5, QTableWidgetItem(row['ask']))
            self.tableWidget.setItem(index, 6, QTableWidgetItem(row['volume']))
            self.tableWidget.setItem(index, 7, QTableWidgetItem(row['openinterest']))
            self.tableWidget.setItem(index, 8, QTableWidgetItem(row['pcratio']))
            index = index + 1

    def export(self):
        pass

    def closeEvent(self, evt):
        print('-------------exit---------')
        event.set()
        os._exit(1)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    qp = QPalette()
    qp.setColor(QPalette.ButtonText, QColor(20, 20, 20))
    qp.setColor(QPalette.WindowText, Qt.white)
    qp.setColor(QPalette.Window, QColor(37, 90, 130))
    qp.setColor(QPalette.Button, Qt.gray)
    app.setPalette(qp)

    # t2.start()

    ex = App()
    sys.exit(app.exec_())