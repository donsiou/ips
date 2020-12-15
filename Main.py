from time import sleep
from thermocoupledao import ThermocoupleDAO
from thermocouple import Thermocouples
from connection import Connection
import threading
import random
import serial

ser=serial.Serial ('com7',9600)

maxTmpValue = 300
minTmpValue = 0
lockRead = threading.Lock()
lockWrite = threading.Lock()
dao = ThermocoupleDAO()
stopThreadRead = False
stopThreadWrite = False
timeSleep = 0


def getDataFromThermocouples():
    '''
        Cette methode return une list de 5 éléments [t1, t2, t3, t4, t5]
    '''
    try:
        X=ser.readline()
        tmp = [X[i] for i in range(5)]
    except Exception:
        tmp = random.sample(range(minTmpValue, maxTmpValue),5)
    return tmp


def getDataFromDb(nbElements):
    return [thermocouple.getValeursTemperature() for thermocouple in dao.findNElements(nbElements)]


def update_plot(object, nbElements):
        # Un variable qui contient les 5 valeurs des thermocouple pour chaque mesure 
        # [ [T1, T2, T3, T4, T5], [T1, T2, T3, T4, T5] .... ]
        listThermocouple = getDataFromDb(nbElements);
        listMoyenThermo = []
        for liste in listThermocouple:
            s = 0
            for temp in liste:
                s += temp
            listMoyenThermo.append(s/5)
        # une variable qui contient 5 liste de nbElements (Une pour chaque thermo)
        # [ [T1, T1, T1, T1, T1], [T2, T2, T2, T2, T2] .... ]
        liste = list(zip(*listThermocouple))
        couleurs = ['r', 'b', 'g', 'y', 'r', 'o']
        i = 0
        object.canvas.axes[1][2].cla()
        #Les cinq premiers axes, chacune pour un termocoupleurs

        for i in range(5):
            c = int(i%3)
            r = int(i/3)
            object.ydata[i] = object.ydata[i][nbElements:] + list(liste[i])
            object.canvas.axes[r][c].cla()  # Clear the canvas.
            object.canvas.axes[r][c].set_title("T{}".format(i+1), y=-0.01)
            object.canvas.axes[r][c].set_ylim([minTmpValue, maxTmpValue])
            object.canvas.axes[r][c].plot(object.xdata[0], object.ydata[i], couleurs[i])
            #object.canvas.axes[1][2].plot(object.xdata[0], object.ydata[i], couleurs[i])
            # Trigger the canvas to update and redraw.
        object.ydata[5] = object.ydata[5][nbElements:] + listMoyenThermo
        object.canvas.axes[1][2].cla()  # Clear the canvas.
        object.canvas.axes[1][2].set_title("AVG", y=-0.01)
        object.canvas.axes[1][2].set_ylim([minTmpValue, maxTmpValue])
        object.canvas.axes[1][2].plot(object.xdata[0], object.ydata[5], 'gold')
        
        object.canvas.draw()






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
        randomlist = getDataFromThermocouples()
        if (randomlist == None): continue
        t1 = Thermocouples(listTemperatures=randomlist)
        lockWrite.acquire()
        dao.create(t1)
        lockWrite.release()
        compteur =  compteur + 1
        if(compteur == nbElements):
            lockWrite.acquire()
            lockRead.release()
            sleep(0.1)
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


