import json
import psycopg2
from database_config import config

schema = "sector"


def db_read_all(table, column):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        # execute a statement
        cursor.execute(f"""SELECT {column} FROM {schema}.{table};""")
        # fetch the data
        result = cursor.fetchall()

        # close the communication with the PostgreSQL
        cursor.close()
        return result
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()


def db_read_value(table, column, value):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        # execute a statement
        cursor.execute(
            f"""SELECT {column} FROM {schema}.{table} WHERE id = {value};""")
        # fetch the data
        result = cursor.fetchone()

        # close the communication with the PostgreSQL
        cursor.close()
        return result
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()


def db_insert_value(table, column, value):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        cursor.execute(
            f"""INSERT INTO {schema}.{table} ({column}) VALUES ({value});""")

        connection.commit()

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()


def db_insert_value_join(table, column, value):
    connection = None
    params = config()
    connection = psycopg2.connect(**params)

    # create a cursor
    cursor = connection.cursor()

    cursor.execute(
        f"""INSERT INTO {schema}.{table} ({column}) VALUES ({value});""")

    connection.commit()

    cursor.close()
    if connection is not None:
        connection.close()


def db_remove_row(table, column, value):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        # update the id value
        cursor.execute(
            f"""DELETE FROM "{table}" WHERE {column} = {value};""")
        connection.commit()

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()


def db_update_value(table, column, value, new_value):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        # update the column value where id is 1
        cursor.execute(
            f"""UPDATE {schema}.{table} SET {column} = '{new_value}' WHERE id = {value};""")
        connection.commit()

        cursor.close()
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()


def dv_check_if_exists(table, column, value):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        # check if the value exists in the column of the table
        cursor.execute(
            f"""SELECT EXISTS(SELECT 1 FROM {schema}.{table} WHERE id = {value});""")
        result = cursor.fetchone()[0]
        connection.commit()

        cursor.close()
        return result
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()


def top_5_from_column(table, value, order, limit):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        cursor.execute(
            f"""SELECT {value} FROM {schema}.{table} ORDER BY {order} DESC LIMIT {limit};""")

        result = cursor.fetchall()  # Fetch all rows instead of just one
        connection.commit()

        cursor.close()
        return result
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()


def get_rank_from_value(table, column, id):
    connection = None
    try:
        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        cursor.execute(
            f"""SELECT COUNT(*) FROM {schema}.{table} WHERE {column} >= (SELECT {column} FROM {schema}.{table} WHERE id = {id});""")
        result = cursor.fetchone()[0]
        connection.commit()

        cursor.close()
        return result
    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()


def join():
    table = "users"
    column = "id, username, join_date, xp, sanctions, roles, badges"
    value = "442729843055132674, 'iqexotic', '2020-02-16', '0', '0', '0', '0'"
    db_insert_value(table, column, value)


def import_json():
    connection = None
    schema = "sector"  # Füge das gewünschte Schema hinzu
    table = "users"

    try:
        # JSON-Datei laden
        with open('xp_data.json') as f:
            data = json.load(f)

        params = config()
        connection = psycopg2.connect(**params)

        # create a cursor
        cursor = connection.cursor()

        for user_id, user_data in data.items():
            # Annahme: Es gibt nur ein XP-Wert-Paar in jedem Eintrag
            xp = list(user_data.values())[0]

            # SQL-Abfrage vorbereiten und ausführen
            sql_query = f"INSERT INTO {schema}.{table} (id, xp) VALUES (%s, %s);"
            cursor.execute(sql_query, (user_id, xp))

        connection.commit()

    except (Exception, psycopg2.DatabaseError) as e:
        print(e)
    finally:
        if connection is not None:
            connection.close()


# Hier rufst du die Funktion auf
import_json()
