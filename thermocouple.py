import time

class Thermocouples:
    def __init__(self, timestamp=None, listTemperatures=[]):
        """
            Une list des températures (List qui contient une autre list de 5 éléments)
        """
        self._listTemperatures = listTemperatures
        self._timestamp = timestamp if timestamp != None else int(
            round(time.time() * 1000))

    def getDateTime(self):
        return self._timestamp
    
    def getValeursTemperature(self):
        return self._listTemperatures[0], self._listTemperatures[1], self._listTemperatures[2], self._listTemperatures[3], self._listTemperatures[4]
