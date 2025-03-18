import logging
from collections import OrderedDict

import mysql.connector
from mysql.connector import Error

from sinks.sink import Sink


class MySQL_Sink(Sink):

    def __init__(self):
        self.ids = {}

    def update(self, new_data: [OrderedDict]):
        connection, cursor = None, None
        try:
            connection, cursor = self.get_connection
            cursor = connection.cursor(buffered=True)

            cursor.execute(
                "CREATE TABLE IF NOT EXISTS meldingen (id VARCHAR(8) PRIMARY KEY, text VARCHAR(255), time_text VARCHAR("
                "255),priority VARCHAR(255), vehicle VARCHAR(255), caps VARCHAR(255), types VARCHAR(255), "
                "lat DOUBLE, lng DOUBLE, street VARCHAR(255), city VARCHAR(255))")

            for data in new_data:
                id = data["id"]
                print(f"id: {id}")
                cursor.execute(f"SELECT * FROM meldingen WHERE id ='{id}'")
                result = cursor.fetchone()
                if result is None:
                    lat = data['lat'] or 0
                    lng = data['lng'] or 0
                    sql = f"INSERT INTO meldingen (id,text,time_text,priority,vehicle,caps,types,lat,lng,street,city) VALUES (" + \
                          f"'{id}', '{data['text']}', '{data['time_text']}', '{data['priority']}', '{data['vehicle']}', '{data['caps']}', " + \
                          f"'{data['types']}', {float(lat)}, {float(lng)}, '{data['street']}', '{data['city']}')"
                    cursor.execute(sql)

                    connection.commit()
        except Error as e:
            logging.error(f"Error while connecting to MySQL: {e}")
        finally:
            if cursor:
                cursor.close()
            if connection:
                connection.close()

    @property
    def get_connection(self):
        connection = mysql.connector.connect(host='localhost',
                                             port=3306,
                                             database='112app',
                                             user='root',
                                             password='CEtbUpkfwvVKF7Cz')
        if not connection.is_connected():
            raise ValueError("Could not connect to the Database!")
        return connection
