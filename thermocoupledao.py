from connection import Connection
from sqlite3 import Error
from datetime import datetime
from thermocouple import Thermocouples


class ThermocoupleDAO:
    
    def __init__(self):
        self._conn = Connection.getInstance().getConnection()

    def createTable(self):
        sql_create_thermocouple_table = """ CREATE TABLE IF NOT EXISTS thermocouple (
                                            id       INTEGER PRIMARY KEY AUTOINCREMENT,
                                            datetime REAL,
                                            t1       DOUBLE,
                                            t2       DOUBLE,
                                            t3       DOUBLE,
                                            t4       DOUBLE,
                                            t5       DOUBLE
                                    ); """
        try:
            c = self._conn.cursor()
            c.execute(sql_create_thermocouple_table)
        except Error as e:
            print("Erreur lors de création de table Tehrmocouple")


    def create(self, thermocouple):
        sql = ''' INSERT INTO thermocouple(datetime, t1, t2, t3, t4, t5)
              VALUES(julianday(?),?,?,?,?,?) '''
        data = (str(thermocouple.getDateTime()), *thermocouple.getValeursTemperature())
        print(data)
        try:
            c = self._conn.cursor()
            c.execute(sql, data)
            self._conn.commit()
        except Error as e:
            print("Erreur lors de l'ajout d'un element à la table Thermocouple")

    
    def find(self, id):
        sql = '''SELECT id, datetime(datetime) as datetime, t1, t2, t3, t4, t5
            FROM `thermocouple`
            WHERE id=?;'''
        try:
            c = self._conn.cursor()
            c.execute(sql, (id,))
            row = c.fetchall()[0]
            return self.rowToObject(row)
        except Error as e:
            print("Erreur lors de lecture d'un element à la table Thermocouple")
        pass

    def findNElements(self, nbElements):
        sql = '''SELECT id, datetime(datetime) as datetime, t1, t2, t3, t4, t5
            FROM `thermocouple`
            ORDER BY id DESC
            LIMIT ?;'''
        try:
            c = self._conn.cursor()
            c.execute(sql, (nbElements,))
            rows = c.fetchall()
            list = []
            for row in rows:
                list.append(self.rowToObject(row))

            return list
        except Error as e:
            print("Erreur lors de l'ajout d'un element à la table Thermocouple")
        pass

    def clear(self):
        sql = 'DELETE FROM thermocouple'
        try:
            c = self._conn.cursor()
            c.execute(sql)
            self._conn.commit()
        except Error as e:
            print("Erreur lors de suppression des éléments de la table Thermocouple")


    def rowToObject(self, row):
        dt = datetime.strptime(row[1], '%Y-%m-%d %H:%M:%S')
        lt = [row[2], row[3], row[4], row[5], row[5]]
        return Thermocouples(datetime=dt, listTemperatures=lt)
       
    