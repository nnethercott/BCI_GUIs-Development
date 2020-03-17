# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'museGUIv2.ui'
#
# Created by: PyQt5 UI code generator 5.13.0
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets
import pylsl
import ble2lsl
from ble2lsl.devices import muse2016
import numpy as np

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setGeometry(QtCore.QRect(610, 20, 171, 51))
        self.pushButton.setObjectName("pushButton")

        self.spinBox = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBox.setGeometry(QtCore.QRect(60, 40, 281, 21))
        self.spinBox.setMinimum(1)
        self.spinBox.setMaximum(300)
        self.spinBox.setObjectName("spinBox")

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setGeometry(QtCore.QRect(610, 90, 171, 51))
        self.pushButton_2.setObjectName("pushButton_2")


        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 26))
        self.menubar.setObjectName("menubar")
        self.menuConfigure = QtWidgets.QMenu(self.menubar)
        self.menuConfigure.setObjectName("menuConfigure")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.actionSettings = QtWidgets.QAction(MainWindow)
        self.actionSettings.setObjectName("actionSettings")
        self.menuConfigure.addAction(self.actionSettings)
        self.menubar.addAction(self.menuConfigure.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #connections
        self.pushButton.clicked.connect(self.startStream)
        self.pushButton_2.clicked.connect(self.record)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "Connect to Device"))
        self.pushButton_2.setText(_translate("MainWindow", "Record"))
        self.menuConfigure.setTitle(_translate("MainWindow", "Configure"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))

    def disable():
        return

    def startStream(self):
        streamer = ble2lsl.Streamer(muse2016)
        if streamer:
            self.pushButton.clicked.connect(self.disable)
            self.pushButton.setText("Connected")
            self.pushButton.setStyleSheet("background-color: #aaaa7f")
            self.pushButton_2.clicked.connect(self.record)

    def record(self):
        stream_info =  pylsl.resolve_byprop("type", "EEG")
        stream = stream_info[0]
        inlet = pylsl.StreamInlet(stream, recover=True)
        inlet.open_stream()
        length=self.spinBox.value()
        
        eeg_data, timestamps = inlet.pull_chunk(
                timeout= length, max_samples=256*length)
        eeg_data = np.array(eeg_data)
        print(eeg_data)



if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
