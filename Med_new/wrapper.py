from datetime import date, datetime, timedelta
import mysql.connector as connection

class wrapper:

    def __init__(self):
        self.cnx = connection.MySQLConnection(user='root', password='root',
                                              host='localhost',
                                              database='medvendo')
        self.cursor = self.cnx.cursor(dictionary=True, buffered=True)

    def insert(self, tablename, **kwargs):
        x = *kwargs,
        y = *kwargs.values(),
        query = "INSERT INTO " + tablename + " " + str(x) + " VALUES " + str(y)
        self.cursor.execute(query)
        return

    def select(self, tablename, **kwargs):
        x = *kwargs,
        y = *kwargs.values(),
        query = "SELECT * FROM " + tablename + " WHERE " + str(x[0]) + " = " + str(y[0])
        return self.cursor.execute(query)