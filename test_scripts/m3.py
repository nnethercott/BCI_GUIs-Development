# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'museGUIv2.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
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

        self.connect_button = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button.setGeometry(QtCore.QRect(610, 20, 171, 51))
        self.connect_button.setObjectName("connect_button")

        self.connect_button2 = QtWidgets.QPushButton(self.centralwidget)
        self.connect_button2.setGeometry(QtCore.QRect(610, 90, 171, 51))
        self.connect_button2.setObjectName("connect_button2")

        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 561, 121))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")

        self.timestamps_box = QtWidgets.QCheckBox(self.centralwidget)
        self.timestamps_box.setGeometry(QtCore.QRect(483, 68, 561, 121))
        self.timestamps_box.setText("Timestamps")
        self.timestamps_box.setObjectName("timestamps_box")

        self.spinBox = QtWidgets.QSpinBox(self.groupBox)
        self.spinBox.setGeometry(QtCore.QRect(80, 40, 191, 22))
        self.spinBox.setObjectName("spinBox")

        self.lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(80, 10, 401, 22))
        self.lineEdit.setObjectName("lineEdit")

        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setGeometry(QtCore.QRect(10, 10, 61, 16))
        self.label.setObjectName("label")

        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setGeometry(QtCore.QRect(10, 40, 55, 16))
        self.label_2.setObjectName("label_2")

        self.browse = QtWidgets.QPushButton(self.groupBox)
        self.browse.setGeometry(QtCore.QRect(490, 10, 61, 21))
        self.browse.setObjectName("browse")

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

        #initial connections
        self.connect_button.clicked.connect(self.startStream)
        self.browse.clicked.connect(self.browseSlot)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connect_button.setText(_translate("MainWindow", "Connect to Device"))
        self.label.setText(_translate("MainWindow", "File Name"))
        self.label_2.setText(_translate("MainWindow", "Duration"))
        self.browse.setText(_translate("MainWindow", "Browse"))
        self.menuConfigure.setTitle(_translate("MainWindow", "Configure"))
        self.actionSettings.setText(_translate("MainWindow", "Settings"))

    def browseSlot( self ):
        ''' Called when the user presses the Browse button
        '''
        #self.debugPrint( "Browse button pressed" )
        options = QtWidgets.QFileDialog.Options()
        options |= QtWidgets.QFileDialog.DontUseNativeDialog
        fileName, _ = QtWidgets.QFileDialog.getSaveFileName(
                        None,
                        "QFileDialog.getOpenFileName()",
                        "",
                        "All Files (*);;Python Files (*.py)",
                        options=options)
        if fileName:
            self.lineEdit.setText(fileName)

    def disable(self):
        return

    def startStream(self):
        streamer = ble2lsl.Streamer(muse2016)
        if streamer:
            self.connect_button.clicked.connect(self.disable)
            self.connect_button.setText("Connected")
            self.connect_button.setStyleSheet("background-color: #aaaa7f")

    def record(self):
        try:
            stream_info =  pylsl.resolve_byprop("type", "EEG")
            stream = stream_info[0]
            inlet = pylsl.StreamInlet(stream, recover=True)
            inlet.open_stream()
            length=self.spinBox.value()
            sr=256

            eeg_data, timestamps = inlet.pull_chunk(
                    timeout= length, max_samples=sr*length)
            eeg_data = np.array(eeg_data)
            print(eeg_data.shape)

            if self.timestamps_box.value() is True:
                timestamps = np.linspace(0,length, length*sr)

        except ConnectionError:
            print('Device not connected')




if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
