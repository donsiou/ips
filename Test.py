import sys
import random
import matplotlib
import Main
from connection import Connection
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, axes = plt.subplots(nrows=2, ncols=3)
        self.axes = axes
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        n_data = 10
        self.xdata = []
        self.ydata = [[], [], [], [], [], []] 
        self.xdata.append(list(range(n_data)))
        self.ydata.append(Main.getDataFromDb(n_data))
        Main.update_plot(self, n_data)

        self.show()

        Main.readWriteDB(self, 10)

        # Setup a timer to trigger the redraw by calling update_plot.
        

    


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
Main.stopThreadRead = True
Main.stopThreadWrite = True
Connection.getInstance().getConnection().close()