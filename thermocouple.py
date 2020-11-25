from datetime import datetime

class Thermocouples:
    def __init__(self, datetime=datetime.now(), listTemperatures=[]):
        """
            Une list des températures (List qui contient une autre list de 5 éléments)
        """
        self._listTemperatures = listTemperatures
        self._datetime = datetime

    def getDateTime(self):
        return self._datetime
    
    def getValeursTemperature(self):
        return self._listTemperatures[0], self._listTemperatures[1], self._listTemperatures[2], self._listTemperatures[3], self._listTemperatures[4]
