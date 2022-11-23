import datetime
import os
import logging
import mysql.connector
from mysql.connector import Error

from azure.storage.queue import (
        QueueClient,
        BinaryBase64EncodePolicy,
        BinaryBase64DecodePolicy
)
import azure.functions as func


def main(mytimer: func.TimerRequest) -> None:
    # Retrieving secrets through environment variables
    DB_HOST = os.getenv('DB_HOST')
    DB_USER = os.getenv('DB_USER')
    DB_PASS = os.getenv('DB_PASS')
    DB_NAME = os.getenv('DB_NAME')

    QUEUE_CONN_STRING = os.getenv("QUEUE_CONN_STRING")
    QUEUE_NAME = os.getenv('QUEUE_NAME')

    # Creating the Storage Queue connection client
    queue_client = QueueClient.from_connection_string(QUEUE_CONN_STRING, QUEUE_NAME)

    # Connecting to the MySQL server
    connection = mysql.connector.connect(host=DB_HOST,
                                        database=DB_NAME,
                                        user=DB_USER,
                                        password=DB_PASS,
                                        port=3306,
                                        ssl_disabled=True)

    # Qurying the SQL Server
    sql_select_Query = "select * from schedules"
    cursor = connection.cursor()
    cursor.execute(sql_select_Query)
    records = cursor.fetchall()

    # Looping through all the schedules and sending messages to the queue for processing
    for row in records:
        # The queue message will be formated for easily format it into a dict
        data = '{"scheduleId": "' + str(row[0]) + '", "userId": "' + str(row[1]) + '", "zipCodes": "' + str(row[4]) + '", "url": "' + str(row[14]) + '"}'
        logging.info(data)
        queue_client.send_message(data)
    
    # If the SQL connection is till active, then close it
    if connection.is_connected():
        connection.close()
        cursor.close()