from datetime import date, datetime, timedelta
import re
import mysql.connector as connection

class Wrapper:

    def __init__(self):
        self.cnx = connection.MySQLConnection(user='root', password='root',
                                              host='localhost',
                                              database='Dispenser')
        self.cnx.autocommit = True
        self.cursor = self.cnx.cursor(dictionary=True,buffered=True,)

    def insert(self, tablename, **kwargs):
        x = *kwargs,
        y = *kwargs.values(),
        query = "INSERT INTO " + tablename + " " + re.sub("['\"]","",str(x)) + " VALUES " + str(y)
        print(query)
        self.cursor.execute(query)
        return

    def select(self, tablename, **kwargs):
        x = *kwargs,
        y = *kwargs.values(),
        query = "SELECT * FROM " + tablename + " WHERE " + str(x[0]) + " = \'" + y[0] + "\'"
        print(query)
        self.cursor.execute(query)
        return self.cursor

    def update(self, tablename, field, value, **kwargs):
        x = *kwargs,
        y = *kwargs.value()
        query = "UPDATE " + tablename + "SET " + str(x[0]) + " = \'" + y[0] + "\' WHERE " + field + " = \'" + value + "\'"
        


