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


def getDataFromDb(nbElements):
    return [thermocouple.getValeursTemperature()for thermocouple in dao.findNElements(nbElements)]


def update_plot(object, nbElements):
        list = getDataFromDb(nbElements)
        couleurs = ['r', 'b', 'g', 'y', 'p', 'o']
        for i in range(6):
            # Drop off the nbElements element, append a new one.
            c = int(i%3)
            r = int(i/3)
            object.ydata[i] = object.ydata[i][nbElements:] + getDataFromDb(nbElements)
            object.canvas.axes[r][c].cla()  # Clear the canvas.
            object.canvas.axes[r][c].plot(object.xdata[0], object.ydata[i], couleurs[i])
            # Trigger the canvas to update and redraw.
            object.canvas.draw()



def readFromDb(object, nbElements):
    while True:
        print("Reading value : ")
        lockRead.acquire()
        update_plot(object,nbElements)
        lockWrite.release()
        sleep(0.5)
   

def addToDb(nbElements):
    compteur = 0
    while True:
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


