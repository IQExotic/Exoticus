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


    def select(self, table: str, fields: list, limit=None, where=None, where_values=None):
        # fields -> ['field1', 'field2']
        # where -> "WHERE user_id = {}"
        # where_values -> [4]  -> "WHERE user_id = 4"
        if where and where_values:
            if limit:
                cursor = self._getCursor()
                where.format(*where_values)
                cursor.execute("SELECT {} FROM {} WHERE {} LIMIT {}};".format(self._formatFields(fields), table, where, limit))
                return cursor.query.decode('utf-8')
            cursor = self._getCursor()
            where.format(*where_values)
            cursor.execute("SELECT {} FROM {} WHERE {};".format(self._formatFields(fields), table, where))
            return cursor.query.decode('utf-8')
        
        if limit:
            cursor = self._getCursor()
            where.format(*where_values)
            cursor.execute("SELECT {} FROM {} LIMIT {};".format(self._formatFields(fields), table, limit))
            return cursor.query.decode('utf-8')
        cursor = self._getCursor()
        cursor.execute("SELECT {} FROM {};".format(self._formatFields(fields), table))
        return cursor.query.decode('utf-8')


    def insert(self, table: str, fields: list, values: list):
        # fields -> ['field1', 'field2']
        # values -> ['value1 for field1', 'value2 for field2']
        cursor = self._getCursor()
        cursor.execute("INSERT INTO {} ({}) VALUES ({});".format(table, self._formatFields(fields), self._formatFields(values)))
        return cursor.query.decode('utf-8')



    def update(self, table: str, fields: str, values: list, where: str, where_values: list):
        # fields -> "column1 = {}, column2 = {}"
        # values -> ['value1 for field1', 'value2 for field2']
        # where -> "WHERE user_id = {}"
        # where_values -> [4]  -> "WHERE user_id = 4"
        cursor = self._getCursor()
        fields.format(*values)
        where.format(*where_values)
        cursor.execute("UPDATE {} SET {} WHERE {};".format(table, fields, where))
        return cursor.query.decode('utf-8')



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
    print("Connection to PostgreSQL database successful.")

        # Pass the connection to your DatabaseManager
    if connection:
        db_manager = DatabaseManger(connection)
        print(db_manager.select("* FROM MYTABLE; --", ["field1", "field2"]))
        print(db_manager.select("MYTABLE", ["field1", "field2"], 5))
        print(db_manager.select("MYTABLE", ["field1", "field2"], 5, "WHERE user_id = {} AND [name] = {}", [10, "John"]))
        print(db_manager.select("MYTABLE", ["field1", "field2"], where="WHERE user_id = {} AND [name] = {}", where_values=[10, "John"]))

except psycopg2.Error as e:
    print("Error connecting to PostgreSQL database:", e)
