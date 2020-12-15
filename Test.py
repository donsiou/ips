import sys
import random
import matplotlib
import Main
from Ui_form import Ui_Main
from PyQt5.QtCore import pyqtSlot
from PyQt5 import QtCore, QtGui, QtWidgets
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

        #Nb Value
        self.boxNbValue = QtWidgets.QVBoxLayout()
        self.txtNbValue = QtWidgets.QLabel()
        self.txtNbValue.setObjectName("txrNbValue")
        self.txtNbValue.setText("Nombre valeurs : 10")
        self.boxNbValue.addWidget(self.txtNbValue)
        self.slideNbValue = QtWidgets.QSlider()
        self.slideNbValue.setOrientation(QtCore.Qt.Horizontal)
        self.slideNbValue.setObjectName("slideNbValue")
        self.slideNbValue.setMinimum(10)
        self.slideNbValue.valueChanged.connect(self.on_slideNbValue_valueChanged)
        self.boxNbValue.addWidget(self.slideNbValue)
        
        #NB Secondes
        self.boxNbSecondes = QtWidgets.QVBoxLayout()
        self.txtNbSecondes = QtWidgets.QLabel()
        self.txtNbSecondes.setObjectName("txtNbSecondes")
        self.txtNbSecondes.setText("Nombres secondes : 10")
        self.boxNbSecondes.addWidget(self.txtNbSecondes)
        self.slideNbSeconde = QtWidgets.QSlider()
        self.slideNbSeconde.setOrientation(QtCore.Qt.Horizontal)
        self.slideNbSeconde.setObjectName("slideNbSeconde")
        self.slideNbSeconde.setMinimum(10)
        self.slideNbSeconde.valueChanged.connect(self.on_slideNbSeconde_valueChanged)
        self.boxNbSecondes.addWidget(self.slideNbSeconde)
        
        #Box Filters
        self.boxFiltres = QtWidgets.QHBoxLayout()

        self.boxFiltres.addLayout(self.boxNbValue, 1)
        self.boxFiltres.addLayout(self.boxNbSecondes, 1)
        self.boxFiltres.addWidget(toolbarAnalyse, 3)
        

        self.boxLive.addWidget(toolbar)
        self.boxLive.addWidget(self.canvas)
        
        self.boxPlotAnalyse.addLayout(self.boxFiltres)
        self.boxPlotAnalyse.addWidget(self.canvasAnalyse, 1)

        n_data = 20
        self.xdata = []
        self.ydata = [[], [], [], [], [], []] 
        self.xdata.append(list(range(n_data)))
        #self.ydata.append(Main.getDataFromDb(n_data))
        Main.update_plot(self, n_data)

        self.show()

        Main.readWriteDB(self, 3)


    @pyqtSlot()
    def on_radioT1_clicked(self):
        if(self.radioT1.isChecked()):
            self.lcdTemp.display(self.ydata[0][-1])

    @pyqtSlot()
    def on_radioT2_clicked(self):
        if(self.radioT2.isChecked()):
            self.lcdTemp.display(self.ydata[1][-1])

    @pyqtSlot()
    def on_radioT3_clicked(self):
        if(self.radioT3.isChecked()):
            self.lcdTemp.display(self.ydata[2][-1])

    @pyqtSlot()
    def on_radioT4_clicked(self):
        if(self.radioT4.isChecked()):
            self.lcdTemp.display(self.ydata[3][-1])

    @pyqtSlot()
    def on_radioT5_clicked(self):
        if(self.radioT5.isChecked()):
            self.lcdTemp.display(self.ydata[4][-1])    
    
    @pyqtSlot()
    def on_slideNbValue_valueChanged(self):
        value = self.slideNbValue.value()
        self.txtNbValue.setText("Nombres valeurs : {}".format(value))

    @pyqtSlot()
    def on_slideNbSeconde_valueChanged(self):
        value = self.slideNbSeconde.value()
        self.txtNbSecondes.setText("Nombres secondes : {}".format(value))


    @pyqtSlot()
    def on_btnUpdate_clicked(self):
        nbElements = self.slideNbValue.value()
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