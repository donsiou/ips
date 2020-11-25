import sys
import random
import matplotlib
import Main
matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        self.setCentralWidget(self.canvas)

        n_data = 10
        self.xdata = list(range(n_data))
        self.ydata = Main.getDataFromDb(n_data)
        Main.update_plot(self, n_data)

        self.show()

        Main.readWriteDB(self, 2)

        # Setup a timer to trigger the redraw by calling update_plot.
        

    


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()