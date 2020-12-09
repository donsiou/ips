import sys
import random
import matplotlib
import Main
from Ui_form import Ui_Main
from PyQt5.QtCore import pyqtSlot
from connection import Connection
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg, NavigationToolbar2QT as NavigationToolbar
from time import sleep
from matplotlib.figure import Figure

matplotlib.use('Qt5Agg')

from PyQt5 import QtCore, QtWidgets

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import matplotlib.pyplot as plt


class MplCanvasLive(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig, axes = plt.subplots(nrows=2, ncols=3)
        self.axes = axes
        super(MplCanvasLive, self).__init__(fig)

class MplCanvasAnalyse(FigureCanvas):
    def __init__(self, parent=None, width=5, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        self.axes.set_title("Thermocouples From Database")
        super(MplCanvasAnalyse, self).__init__(fig)


class MainWindow(QtWidgets.QMainWindow, Ui_Main):

    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        Ui_Main.__init__(self)
        self.setupUi(self)
        self.canvas = MplCanvasLive(self, width=5, height=4, dpi=100)
        self.canvasAnalyse = MplCanvasAnalyse(self, width=5, height=4, dpi=100)
        #self.setCentralWidget(self.canvas)
        toolbar = NavigationToolbar(self.canvas, self)
        toolbarAnalyse = NavigationToolbar(self.canvasAnalyse, self)
        self.boxLive.addWidget(toolbar)
        self.boxLive.addWidget(self.canvas)
        
        self.boxPlotAnalyse.addWidget(toolbarAnalyse)
        self.boxPlotAnalyse.addWidget(self.canvasAnalyse)

        n_data = 10
        self.xdata = []
        self.ydata = [[], [], [], [], [], []] 
        self.xdata.append(list(range(n_data)))
        #self.ydata.append(Main.getDataFromDb(n_data))
        Main.update_plot(self, n_data)

        self.show()

        Main.readWriteDB(self, 1)

    @pyqtSlot()
    def on_btnUpdate_clicked(self):
        nbElements = 10
        dataAllThermo = Main.getDataFromDb(nbElements)
        listLegends = []
        self.canvasAnalyse.axes.cla()
        xData = list(range(nbElements))
        if(self.checkT1.isChecked()):
            dataT1 = [data[0] for data in dataAllThermo]
            self.canvasAnalyse.axes.plot(xData, dataT1, 'm')
            listLegends.append("T1")
        if(self.checkT2.isChecked()):
            dataT2 = [data[1] for data in dataAllThermo]
            self.canvasAnalyse.axes.plot(xData, dataT2, 'b')
            listLegends.append("T2")
        if(self.checkT3.isChecked()):
            dataT3 = [data[2] for data in dataAllThermo]
            self.canvasAnalyse.axes.plot(xData, dataT3, 'g')
            listLegends.append("T3")
        if(self.checkT4.isChecked()):
            dataT4 = [data[3] for data in dataAllThermo]
            self.canvasAnalyse.axes.plot(xData, dataT4, 'y')
            listLegends.append("T4")
        if(self.checkT5.isChecked()):
            dataT5 = [data[4] for data in dataAllThermo]
            self.canvasAnalyse.axes.plot(xData, dataT5, 'r')
            listLegends.append("T5")
        self.canvasAnalyse.axes.set_ylim([Main.minTmpValue, Main.maxTmpValue])
        self.canvasAnalyse.axes.set_title("Thermocouples From Database")
        self.canvasAnalyse.axes.legend(listLegends)
        self.canvasAnalyse.draw()
        
        
        

        

    


app = QtWidgets.QApplication(sys.argv)
w = MainWindow()
app.exec_()
Main.stopThreadRead = True
Main.stopThreadWrite = True
sleep(2)
Connection.getInstance().getConnection().close()