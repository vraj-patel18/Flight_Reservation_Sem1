from database import connect_db
from seat import show_seats, read_seats, update_seat
import random
import string


def book_seat():
    import random
    import string

    customer_id = int(input("Customer ID: "))
    flight_no = input("Flight number: ").upper()

    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "SELECT id FROM customers WHERE id = %s",
        (customer_id,)
    )
    customer = cursor.fetchone()

    cursor.execute(
        "SELECT id, fare, seat_file FROM flights WHERE flight_no = %s",
        (flight_no,)
    )
    flight = cursor.fetchone()

    if customer is None:
        print("Customer not found.")

    elif flight is None:
        print("Flight not found.")

    else:
        flight_id = flight[0]
        fare = flight[1]
        seat_file = flight[2]

        show_seats(seat_file)

        seat_no = input("Choose a seat (example 2B): ").upper()

        seats = read_seats(seat_file)

        try:
            row_number = int(seat_no[:-1])
            letter = seat_no[-1]
            letters = seats[0][1:]

            if row_number < 1 or row_number >= len(seats):
                print("Invalid seat number.")

            elif letter not in letters:
                print("Invalid seat letter.")

            else:
                column = letters.index(letter) + 1

                if seats[row_number][column] != "Available":
                    print("Seat is already booked.")

                else:
                    # Generate a 6-character PNR
                    pnr = ''.join(
                        random.choices(
                            string.ascii_uppercase + string.digits,
                            k=6
                        )
                    )

                    # Mark the seat as booked in the CSV file
                    update_seat(seat_file, seat_no, "Booked")

                    try:
                        cursor.execute(
                            """INSERT INTO bookings
                            (pnr, customer_id, flight_id, seat_no, status)
                            VALUES (%s, %s, %s, %s, %s)""",
                            (
                                pnr,
                                customer_id,
                                flight_id,
                                seat_no,
                                "Confirmed"
                            )
                        )

                        db.commit()

                        print("\n===== BOOKING CONFIRMED =====")
                        print("PNR Number :", pnr)
                        print("Flight      :", flight_no)
                        print("Seat Number :", seat_no)
                        print("Ticket Fare : Rs.", fare)
                        print("Status      : Confirmed")

                    except Exception as error:
                        db.rollback()
                        update_seat(seat_file, seat_no, "Available")
                        print("Booking failed:", error)

        except (ValueError, IndexError):
            print("Invalid seat format. Example: 2B")

    cursor.close()
    db.close()

def view_booking():
    pnr = input("Enter PNR: ")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT bookings.pnr, customers.name, flights.flight_no,
        flights.source, flights.destination, flights.flight_date,
        bookings.seat_no, flights.fare, bookings.status
        FROM bookings JOIN customers ON bookings.customer_id=customers.id
        JOIN flights ON bookings.flight_id=flights.id WHERE bookings.pnr=%s""", (pnr,))
    booking = cursor.fetchone()
    print(booking if booking else "Booking not found.")
    cursor.close()
    db.close()

def cancel_booking():
    pnr = input("Enter PNR to cancel: ")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT bookings.seat_no, bookings.status, flights.seat_file
        FROM bookings JOIN flights ON bookings.flight_id=flights.id
        WHERE bookings.pnr=%s""", (pnr,))
    booking = cursor.fetchone()
    if booking is None:
        print("Booking not found.")
    elif booking[1] == "Cancelled":
        print("Booking already cancelled.")
    else:
        update_seat(booking[2], booking[0], "Available")
        cursor.execute("UPDATE bookings SET status='Cancelled' WHERE pnr=%s", (pnr,))
        db.commit()
        print("Booking cancelled.")
    cursor.close()
    db.close()

def booking_history():
    customer_id = int(input("Customer ID: "))
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("""SELECT bookings.pnr, flights.flight_no, flights.source,
        flights.destination, bookings.seat_no, bookings.status
        FROM bookings JOIN flights ON bookings.flight_id=flights.id
        WHERE bookings.customer_id=%s""", (customer_id,))
    bookings = cursor.fetchall()
    if not bookings:
        print("No booking history found.")
    for booking in bookings:
        print(booking)
    cursor.close()
    db.close()

def view_seat_matrix():
    flight_no = input("Flight number: ").upper()
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT seat_file FROM flights WHERE flight_no=%s", (flight_no,))
    result = cursor.fetchone()
    if result is None:
        print("Flight not found.")
    else:
        show_seats(result[0])
    cursor.close()
    db.close()
