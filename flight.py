from database import connect_db
from seat import create_seat_file

def add_flight():
    flight_no = input("Flight number: ").upper()
    source = input("Source city: ")
    destination = input("Destination city: ")
    flight_date = input("Flight date (YYYY-MM-DD): ")
    fare = float(input("Fare: "))
    rows = int(input("Number of seat rows: "))
    columns = int(input("Seats per row (4 or 6): "))
    if rows < 1 or columns not in (4, 6):
        print("Use at least one row and either 4 or 6 seats per row.")
        return
    seat_file = create_seat_file(flight_no, rows, columns)
    db = connect_db()
    cursor = db.cursor()
    try:
        cursor.execute("INSERT INTO flights (flight_no, source, destination, flight_date, fare, seat_file) VALUES (%s, %s, %s, %s, %s, %s)", (flight_no, source, destination, flight_date, fare, seat_file))
        db.commit()
        print("Flight added.")
    except Exception as error:
        db.rollback()
        print("Could not add flight:", error)
    cursor.close()
    db.close()

def view_flights():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM flights")
    flights = cursor.fetchall()
    if not flights:
        print("No flights found.")
    for flight in flights:
        print(flight)
    cursor.close()
    db.close()

def search_flight():
    source = input("Source city: ")
    destination = input("Destination city: ")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM flights WHERE source=%s AND destination=%s", (source, destination))
    flights = cursor.fetchall()
    if not flights:
        print("No matching flights found.")
    for flight in flights:
        print(flight)
    cursor.close()
    db.close()
