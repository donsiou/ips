import sqlite3
from sqlite3 import Error

class Connection:
    connection = None

    @staticmethod
    def getInstance():
        if not Connection.connection:
            Connection.connection = Connection("thermocouple.db")
        return Connection.connection

    def __init__(self, dbfile):
        try:
            self._conn = sqlite3.connect(dbfile, check_same_thread=False)
            print(sqlite3.version)
        except Error as e:
            print(e)

    def getConnection(self):
        return self._conn

    
    
    
con = Connection.getInstance()