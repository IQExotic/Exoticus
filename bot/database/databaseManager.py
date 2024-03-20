#import mysql.connector as mysqlc

import psycopg2

class DatabaseManger:
    def __init__(self, connection):
        """
        connection = mysqlc.connect(host='localhost',
                             database='python_db',
                             user='pynative',
                             password='pynative@#29')
        """
        self.connection = connection

    def _getCursor(self):
        #return self.connection.cursor(prepared=True)
        return self.connection.cursor()
    
    
    def _formatFields(self, fields: list) -> str:
        if len(fields) == 0:
            return "*"
        return ", ".join(fields)
    
    def closeConnetion(self):
        self.connection.close()


    def select(self, table: str, fields: list, data: dict, limit=None, where=None):
        # fields -> "column1, column2"
        # value -> "value1, value2"
        # data -> {"user_id": 10}
        # where -> "WHERE user_id = %(user_id)d"
        if where:
            if limit:
                cursor = self._getCursor()
                q = cursor.mogrify("SELECT {} FROM {} WHERE {} LIMIT {}};".format(self._formatFields(fields), table, where, limit), data)
                return q.decode('utf-8')
            
            cursor = self._getCursor()
            cursor.mogrify("SELECT {} FROM {} WHERE {};".format(self._formatFields(fields), table, where), data)
            return q.decode('utf-8')
        
        if limit:
            cursor = self._getCursor()
            cursor.mogrify("SELECT {} FROM {} LIMIT {};".format(self._formatFields(fields), table, limit), data)
            return q.decode('utf-8')
        
        cursor = self._getCursor()
        q = cursor.mogrify("SELECT {} FROM {};".format(self._formatFields(fields), table), data)
        return q.decode('utf-8')


    def insert(self, table: str, fields: list, value: str, data: dict):
        # fields -> "column1, column2"
        # value -> "value1, value2"
        # data -> {"user_id": 10}
        cursor = self._getCursor()
        q = cursor.mogrify("INSERT INTO {} ({}) VALUES ({});".format(table, self._formatFields(fields), value), data)
        return q.decode('utf-8')



    def update(self, table: str, fields: str, where: str, data: dict):
        # fields -> "column1 = %(value1)s, column2 = %(value2)s"
        # where -> "WHERE user_id = %(user_id)d"
        # data ->  {"user_id": 10}
        cursor = self._getCursor()
        q = cursor.mogrify("UPDATE {} SET {} WHERE {};".format(table, fields, where), data)
        return q.decode('utf-8')


"""

db_params = {
    'host': 'localhost',
    'database': 'jcorechat-db',
    'user': 'jcorechat',
    'password': 'app_api',
    'port': 5433
}

# Establish connection
try:
    connection = psycopg2.connect(**db_params)
    connection.set_session(autocommit=False)
    print("Connection to PostgreSQL database successful.")

        # Pass the connection to your DatabaseManager
    if connection:
        db_manager = DatabaseManger(connection)
        print(db_manager.select("myTabel", ["field1", "field2%(username)s"], {"username": "John"}))
        
except psycopg2.Error as e:
    print("Error connecting to PostgreSQL database:", e)

"""

