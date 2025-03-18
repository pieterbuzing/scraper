from unittest import TestCase
from mysql.connector import Error

from sinks.MySQL_Sink import MySQL_Sink


class TestMySQL_Sink(TestCase):
    def test_update(self):
        sink = MySQL_Sink()
        try:
            connection = sink.get_connection
            cursor = connection.cursor(buffered=True)
            if connection.is_connected():
                db_Info = connection.get_server_info()
                print("Connected to MySQL Server version ", db_Info)
                cursor = connection.cursor()
                cursor.execute("select database();")
                record = cursor.fetchone()
                print("You're connected to database: ", record)

        except Error as e:
            print("Error while connecting to MySQL", e)
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
                print("MySQL connection is closed")
