from datetime import date, datetime, timedelta
import re
import mysql.connector as connection

class Wrapper:

    def __init__(self):
        self.cnx = connection.MySQLConnection(user='root', password='root',
                                              host='localhost',
                                              database='Dispenser')
        self.cnx.autocommit = True
        self.cursor = self.cnx.cursor(dictionary=True,buffered=True)

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
        if len(x) > 1:
            query = "SELECT * FROM " + tablename + " WHERE "
            for i in range(len(x)):
                query = query + str(x[i]) + " = \'" + str(y[i]) + "\'"
                if i < len(x) - 1:
                    query = query + " AND "
        elif len(x) == 1:
            query = "SELECT * FROM " + tablename + " WHERE " + str(x[0]) + " = \'" + str(y[0]) + "\'"
        else:
            query = "SELECT * FROM " + tablename
        print(query)
        self.cursor.execute(query)
        return self.cursor

    def update(self, tablename, field, value, **kwargs):
        x = *kwargs,
        y = *kwargs.values(),
        query = "UPDATE " + tablename + " SET " + str(x[0]) + " = \'" + str(y[0]) + "\' WHERE " + str(field) + " = \'" + str(value) + "\'"
        print(query)
        self.cursor.execute(query)
        return
