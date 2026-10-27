
import mysql.connector

def connect_db():
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="root@123",
        database="flight_reservation"
    )
    return db