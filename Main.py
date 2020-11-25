from time import sleep
from thermocoupledao import ThermocoupleDAO
from thermocouple import Thermocouples
from connection import Connection
import threading
import random
import time

lockRead = threading.Lock()
lockWrite = threading.Lock()
dao = ThermocoupleDAO()
stopThreadRead = False
stopThreadWrite = False
timeSleep = 0.5


def getDataFromDb(nbElements):
    return [thermocouple.getValeursTemperature() for thermocouple in dao.findNElements(nbElements)]


def update_plot(object, nbElements):
        liste = list(zip(*getDataFromDb(nbElements)))
        couleurs = ['r', 'b', 'g', 'y', 'r', 'o']
        i = 0
        object.canvas.axes[1][2].cla()
        #Les cinq premiers axes, chacune pour un termocoupleurs
        for i in range(5):
            c = int(i%3)
            r = int(i/3)
            object.ydata[i] = object.ydata[i][nbElements:] + list(liste[i])
            object.canvas.axes[r][c].cla()  # Clear the canvas.
            object.canvas.axes[r][c].plot(object.xdata[0], object.ydata[i], couleurs[i])
            object.canvas.axes[1][2].plot(object.xdata[0], object.ydata[i], couleurs[i])
            # Trigger the canvas to update and redraw.
            object.canvas.draw()
        
        #Pour la dérniére on va mettre tout pour comparer






def readFromDb(object, nbElements):
    while not stopThreadRead:
        print("Reading value : ")
        lockRead.acquire()
        update_plot(object,nbElements)
        lockWrite.release()
        sleep(timeSleep)
   

def addToDb(nbElements):
    compteur = 0
    while not stopThreadWrite:
        print("Writing value : ")
        #Generate 5 random numbers between 10 and 30
        randomlist = random.sample(range(10, 30), 5)
        t1 = Thermocouples(listTemperatures=randomlist)
        lockWrite.acquire()
        dao.create(t1)
        lockWrite.release()
        compteur =  compteur + 1
        if(compteur == nbElements):
            lockWrite.acquire()
            lockRead.release()
            compteur = 0

    



def readWriteDB(object, nbElements):
    # Connexion et creation de la table
    dao.clear()
    lockRead.acquire()
    # Workspace
    xRead = threading.Thread(target=readFromDb, args=(object, nbElements,))
    xRead.start()
    xWrite = threading.Thread(target=addToDb, args=(nbElements,))
    xWrite.start()


