import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QMenu, QVBoxLayout, QSizePolicy, QMessageBox, QWidget, QPushButton
from PyQt5.QtGui import QIcon


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt
import numpy as np


class App(QMainWindow):

    def __init__(self):
        super().__init__()
        self.left = 10
        self.top = 10
        self.title = 'PyQt5 matplotlib example - pythonspot.com'
        self.width = 640
        self.height = 400
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        m = PlotCanvas(self, width=300, height=250)
        m.move(100,100)

        button = QPushButton('PyQt5 button', self)
        button.setToolTip('This s an example button')
        button.move(500,0)
        button.resize(140,100)
        button.clicked.connect(m.plot)

        self.show()


class PlotCanvas(FigureCanvas):
    #3-digit thing specifies numrows numcols and index
    #could use this to add 5 plots for all channels
    #figure out how to change the facecolour later :(
    def __init__(self, parent=None, width=300, height=250, dpi=100):
        fig = Figure(figsize=(width/dpi, height/dpi), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.grid()

        FigureCanvas.__init__(self, fig)
        self.setParent(parent)

        FigureCanvas.setSizePolicy(self,
                QSizePolicy.Expanding,
                QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)


    def plot(self,data):
        ax = self.figure.add_subplot(111)
        ax.cla()
        ax.grid(axis='both')
        for i in range(data.shape[1]):
            ax.plot(data[:,i])
        #ax.set_title('PyQt Matplotlib Example')
        self.draw()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
