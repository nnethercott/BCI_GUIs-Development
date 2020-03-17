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
        self.record_button = QtWidgets.QPushButton(self.centralwidget)
        self.record_button.setGeometry(QtCore.QRect(610, 90, 171, 51))
        self.record_button.setObjectName("record_button")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 561, 121))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.time_spinbox = QtWidgets.QSpinBox(self.groupBox)
        self.time_spinbox.setGeometry(QtCore.QRect(80, 40, 191, 22))
        self.time_spinbox.setObjectName("time_spinbox")
        self.file_search = QtWidgets.QLineEdit(self.groupBox)
        self.file_search.setGeometry(QtCore.QRect(80, 10, 401, 22))
        self.file_search.setObjectName("file_search")
        self.file_label = QtWidgets.QLabel(self.groupBox)
        self.file_label.setGeometry(QtCore.QRect(10, 10, 61, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.file_label.setFont(font)
        self.file_label.setObjectName("file_label")
        self.duration_label = QtWidgets.QLabel(self.groupBox)
        self.duration_label.setGeometry(QtCore.QRect(10, 40, 55, 16))
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        self.duration_label.setFont(font)
        self.duration_label.setObjectName("duration_label")
        self.browse_button = QtWidgets.QPushButton(self.groupBox)
        self.browse_button.setGeometry(QtCore.QRect(490, 10, 61, 21))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.browse_button.setFont(font)
        self.browse_button.setObjectName("browse_button")
        self.timestamps_box = QtWidgets.QCheckBox(self.groupBox)
        self.timestamps_box.setGeometry(QtCore.QRect(460, 90, 101, 20))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.timestamps_box.setFont(font)
        self.timestamps_box.setObjectName("timestamps_box")
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
        self.configure_settings_options = QtWidgets.QAction(MainWindow)
        self.configure_settings_options.setObjectName("configure_settings_options")
        self.menuConfigure.addAction(self.configure_settings_options)
        self.menubar.addAction(self.menuConfigure.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        #initial connections
        self.time_spinbox.setMinimum(1)
        self.connect_button.clicked.connect(self.startStream)
        self.browse_button.clicked.connect(self.browseSlot)
        self.record_button.clicked.connect(self.record)


    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.connect_button.setText(_translate("MainWindow", "Connect to Device"))
        self.record_button.setText(_translate("MainWindow", "Record"))
        self.file_label.setText(_translate("MainWindow", "File Name"))
        self.duration_label.setText(_translate("MainWindow", "Duration"))
        self.browse_button.setText(_translate("MainWindow", "Browse"))
        self.timestamps_box.setText(_translate("MainWindow", "Timestamps"))
        self.menuConfigure.setTitle(_translate("MainWindow", "Configure"))
        self.configure_settings_options.setText(_translate("MainWindow", "Settings"))

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
            self.file_search.setText(fileName)

    def disable(self):
        return

    def startStream(self):
        streamer = ble2lsl.Streamer(muse2016)
        if streamer:
            self.connect_button.clicked.connect(self.disable)
            self.connect_button.setText("Connected")
            self.connect_button.setStyleSheet("background-color: #aaaa7f")

    def record(self):
        import pandas as pd

        stream_info =  pylsl.resolve_byprop("type", "EEG")
        stream = stream_info[0]
        inlet = pylsl.StreamInlet(stream, recover=True)
        inlet.open_stream()
        length=self.time_spinbox.value()
        print(length)
        sr=256

        eeg_data, timestamps = inlet.pull_chunk(
                timeout= length, max_samples=sr*length)
        eeg_data = np.squeeze(np.array(eeg_data))

        if self.timestamps_box.isChecked():
            timestamps = np.linspace(0,int(length), int(length)*sr)


        data = pd.DataFrame()
        if timestamps is not None:
            data["time"] = timestamps
        data['s1'] = eeg_data[:,0]
        data['s2'] = eeg_data[:,1]
        data['s3'] = eeg_data[:,2]
        data['s4'] = eeg_data[:,3]
        data['s5'] = eeg_data[:,4]

        data.to_csv(self.file_search.text(), index=False)


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
