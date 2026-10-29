import tkinter as tk
from tkinter import messagebox
from database import connect_db
import csv
import os
import random
import string

SEAT_FOLDER = "seat_matrices"


def show_output(title, lines):
    result.delete("1.0", tk.END)
    result.insert(tk.END, title + "\n" + "=" * 45 + "\n\n")
    result.insert(tk.END, "\n".join(lines))


def add_customer():
    name = input_name.get().strip()
    age = input_age.get().strip()
    phone = input_phone.get().strip()
    if not name or not age or not phone:
        messagebox.showerror("Error", "Enter all customer details")
        return
    try:
        age = int(age)
        if age <= 0:
            messagebox.showerror("Error", "Age must be greater than zero")
            return
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("INSERT INTO customers (name, age, phone) VALUES (%s, %s, %s)", (name, age, phone))
        db.commit()
        cursor.close()
        db.close()
        input_name.delete(0, tk.END)
        input_age.delete(0, tk.END)
        input_phone.delete(0, tk.END)
        messagebox.showinfo("Success", "Customer added successfully")
    except ValueError:
        messagebox.showerror("Error", "Age must be a number")
    except Exception as error:
        messagebox.showerror("Database Error", str(error))


def view_customers():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM customers")
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        lines = []
        for row in rows:
            lines.append(f"Customer ID: {row[0]}\nName: {row[1]}\nAge: {row[2]}\nPhone: {row[3]}\n" + "-" * 45)
        show_output("CUSTOMER DETAILS", lines or ["No customers found."])
    except Exception as error:
        messagebox.showerror("Database Error", str(error))


def create_seat_file(flight_no):
    os.makedirs(SEAT_FOLDER, exist_ok=True)
    path = os.path.join(SEAT_FOLDER, flight_no + ".csv")
    with open(path, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(["Row", "A", "B", "C", "D"])
        for number in range(1, 6):
            writer.writerow([number, "Available", "Available", "Available", "Available"])
    return path


def add_flight():
    flight_no = input_flight.get().strip().upper()
    source = input_source.get().strip()
    destination = input_destination.get().strip()
    date = input_date.get().strip()
    fare_text = input_fare.get().strip()
    if not all([flight_no, source, destination, date, fare_text]):
        messagebox.showerror("Error", "Enter all flight details")
        return
    try:
        fare = float(fare_text)
        if fare < 0:
            messagebox.showerror("Error", "Fare cannot be negative")
            return
        seat_file = create_seat_file(flight_no)
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            "INSERT INTO flights (flight_no, source, destination, flight_date, fare, seat_file) VALUES (%s, %s, %s, %s, %s, %s)",
            (flight_no, source, destination, date, fare, seat_file)
        )
        db.commit()
        cursor.close()
        db.close()
        for field in [input_flight, input_source, input_destination, input_date, input_fare]:
            field.delete(0, tk.END)
        messagebox.showinfo("Success", "Flight added and seat matrix created")
    except ValueError:
        messagebox.showerror("Error", "Enter a valid fare")
    except Exception as error:
        messagebox.showerror("Database Error", str(error))


def view_flights():
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT * FROM flights")
        rows = cursor.fetchall()
        cursor.close()
        db.close()
        lines = []
        for row in rows:
            lines.append(f"Flight ID: {row[0]}\nFlight: {row[1]}\nFrom: {row[2]}\nTo: {row[3]}\nDate: {row[4]}\nFare: Rs. {row[5]}\n" + "-" * 45)
        show_output("FLIGHT DETAILS", lines or ["No flights found."])
    except Exception as error:
        messagebox.showerror("Database Error", str(error))


def find_seat_file(saved_path):
    if saved_path and os.path.exists(saved_path):
        return saved_path
    path = os.path.join(SEAT_FOLDER, os.path.basename(saved_path or ""))
    if os.path.exists(path):
        return path
    return None


def show_seat_layout():
    """Display available and booked seats for the entered flight."""
    flight_no = input_booking_flight.get().strip().upper()
    if not flight_no:
        messagebox.showerror("Error", "Enter the Flight Number first")
        return

    db = None
    cursor = None
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT seat_file FROM flights WHERE flight_no = %s", (flight_no,))
        flight = cursor.fetchone()
        if flight is None:
            messagebox.showerror("Error", "Flight not found")
            return

        path = find_seat_file(flight[0])
        if path is None:
            messagebox.showerror("Error", "Seat CSV file not found for this flight")
            return

        with open(path, "r", newline="") as file:
            seats = list(csv.reader(file))

        if len(seats) < 2 or len(seats[0]) < 2:
            messagebox.showerror("Error", "Seat matrix is empty or invalid")
            return

        seat_window = tk.Toplevel(window)
        seat_window.title("Seat Layout - " + flight_no)
        seat_window.geometry("430x390")
        seat_window.configure(bg="#F1F5F9")
        seat_window.transient(window)

        tk.Label(
            seat_window, text=f"Seat Layout: {flight_no}",
            font=("Arial", 16, "bold"), bg="#172554", fg="white", pady=12
        ).pack(fill="x")

        legend = tk.Frame(seat_window, bg="#F1F5F9")
        legend.pack(pady=10)
        tk.Label(legend, text="Available", bg="#16A34A", fg="white", padx=8, pady=4).pack(side="left", padx=5)
        tk.Label(legend, text="Booked", bg="#DC2626", fg="white", padx=8, pady=4).pack(side="left", padx=5)

        grid_frame = tk.Frame(seat_window, bg="#F1F5F9", padx=15, pady=10)
        grid_frame.pack()
        tk.Label(grid_frame, text="Row", bg="#F1F5F9", font=("Arial", 9, "bold")).grid(row=0, column=0, padx=5, pady=5)
        for col_index, letter in enumerate(seats[0][1:], start=1):
            tk.Label(grid_frame, text=letter, bg="#F1F5F9", font=("Arial", 10, "bold")).grid(row=0, column=col_index, padx=5, pady=5)

        def select_seat(seat_name, seat_status):
            if seat_status.strip().lower() != "available":
                messagebox.showwarning("Seat Unavailable", f"Seat {seat_name} is already booked", parent=seat_window)
                return
            input_seat_no.delete(0, tk.END)
            input_seat_no.insert(0, seat_name)
            seat_window.destroy()

        for row_index in range(1, len(seats)):
            if not seats[row_index]:
                continue
            row_label = seats[row_index][0]
            tk.Label(grid_frame, text=row_label, bg="#F1F5F9").grid(row=row_index, column=0, padx=5, pady=5)
            for col_index, letter in enumerate(seats[0][1:], start=1):
                if col_index >= len(seats[row_index]):
                    continue
                status = seats[row_index][col_index].strip()
                seat_name = f"{row_label}{letter}"
                available = status.lower() == "available"
                tk.Button(
                    grid_frame, text=seat_name, width=5,
                    bg="#16A34A" if available else "#DC2626",
                    fg="white", activeforeground="white",
                    relief="flat", font=("Arial", 9, "bold"),
                    command=lambda name=seat_name, state=status: select_seat(name, state)
                ).grid(row=row_index, column=col_index, padx=4, pady=4)

        tk.Label(
            seat_window, text="Click a green seat to select it.",
            bg="#F1F5F9", fg="#334155", font=("Arial", 10)
        ).pack(pady=(0, 12))

    except Exception as error:
        messagebox.showerror("Seat Layout Error", str(error))
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def book_ticket():
    customer_text = input_customer_id.get().strip()
    flight_no = input_booking_flight.get().strip().upper()
    seat_no = input_seat_no.get().strip().upper()
    if not customer_text or not flight_no:
        messagebox.showerror("Error", "Enter Customer ID and Flight Number")
        return
    if not seat_no:
        show_seat_layout()
        return
    try:
        customer_id = int(customer_text)
    except ValueError:
        messagebox.showerror("Error", "Customer ID must be a number")
        return

    db = None
    cursor = None
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute("SELECT id FROM customers WHERE id = %s", (customer_id,))
        customer = cursor.fetchone()
        cursor.execute("SELECT id, seat_file FROM flights WHERE flight_no = %s", (flight_no,))
        flight = cursor.fetchone()
        if customer is None:
            messagebox.showerror("Error", "Customer ID not found")
            return
        if flight is None:
            messagebox.showerror("Error", "Flight not found")
            return

        flight_id, saved_path = flight
        path = find_seat_file(saved_path)
        if path is None:
            messagebox.showerror("Error", "Seat CSV file not found for this flight")
            return

        with open(path, "r", newline="") as file:
            seats = list(csv.reader(file))
        if len(seats) < 2 or not seats[0]:
            messagebox.showerror("Error", "Seat matrix is empty or invalid")
            return

        row_text, letter = seat_no[:-1], seat_no[-1:]
        if not row_text.isdigit() or letter not in seats[0][1:]:
            messagebox.showerror("Error", "Invalid seat number. Example: 1A")
            return
        row_index = int(row_text)
        column_index = seats[0].index(letter)
        if row_index < 1 or row_index >= len(seats) or column_index >= len(seats[row_index]):
            messagebox.showerror("Error", "Seat does not exist")
            return
        if seats[row_index][column_index].strip().lower() != "available":
            messagebox.showerror("Error", "This seat is already booked")
            return

        pnr = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
        cursor.execute("SELECT pnr FROM bookings WHERE pnr = %s", (pnr,))
        while cursor.fetchone() is not None:
            pnr = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
            cursor.execute("SELECT pnr FROM bookings WHERE pnr = %s", (pnr,))

        cursor.execute(
            "INSERT INTO bookings (pnr, customer_id, flight_id, seat_no, status) VALUES (%s, %s, %s, %s, %s)",
            (pnr, customer_id, flight_id, seat_no, "Confirmed")
        )
        seats[row_index][column_index] = "Booked"
        with open(path, "w", newline="") as file:
            csv.writer(file).writerows(seats)
        db.commit()

        show_output("TICKET BOOKED SUCCESSFULLY", [
            f"PNR: {pnr}", f"Customer ID: {customer_id}",
            f"Flight Number: {flight_no}", f"Seat Number: {seat_no}",
            "Status: Confirmed"
        ])
        messagebox.showinfo("Booking Successful", f"Ticket booked!\nYour PNR is {pnr}")
        input_customer_id.delete(0, tk.END)
        input_booking_flight.delete(0, tk.END)
        input_seat_no.delete(0, tk.END)
    except Exception as error:
        if db:
            db.rollback()
        messagebox.showerror("Booking Error", str(error))
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def view_booking():
    pnr = input_pnr.get().strip().upper()
    if not pnr:
        messagebox.showerror("Error", "Please enter the PNR")
        return
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            """SELECT bookings.pnr, customers.name, flights.flight_no, flights.source,
            flights.destination, bookings.seat_no, bookings.status
            FROM bookings JOIN customers ON bookings.customer_id = customers.id
            JOIN flights ON bookings.flight_id = flights.id WHERE bookings.pnr = %s""",
            (pnr,)
        )
        row = cursor.fetchone()
        cursor.close()
        db.close()
        if row:
            show_output("BOOKING DETAILS", [
                f"PNR: {row[0]}", f"Customer: {row[1]}", f"Flight: {row[2]}",
                f"From: {row[3]}", f"To: {row[4]}", f"Seat: {row[5]}", f"Status: {row[6]}"
            ])
        else:
            show_output("BOOKING DETAILS", ["Booking not found."])
    except Exception as error:
        messagebox.showerror("Database Error", str(error))


def cancel_booking():
    pnr = input_pnr.get().strip().upper()
    if not pnr:
        messagebox.showerror("Error", "Please enter the PNR")
        return
    db = None
    cursor = None
    try:
        db = connect_db()
        cursor = db.cursor()
        cursor.execute(
            """SELECT flights.seat_file, bookings.seat_no FROM bookings
            JOIN flights ON bookings.flight_id = flights.id
            WHERE bookings.pnr = %s AND bookings.status = 'Confirmed'""",
            (pnr,)
        )
        booking = cursor.fetchone()
        if booking is None:
            messagebox.showerror("Error", "Booking not found or already cancelled")
            return

        path = find_seat_file(booking[0])
        seat_no = booking[1]
        if path:
            with open(path, "r", newline="") as file:
                seats = list(csv.reader(file))
            row_text, letter = seat_no[:-1], seat_no[-1:]
            if row_text.isdigit() and letter in seats[0][1:]:
                row_index = int(row_text)
                column_index = seats[0].index(letter)
                if 0 < row_index < len(seats) and column_index < len(seats[row_index]):
                    seats[row_index][column_index] = "Available"
                    with open(path, "w", newline="") as file:
                        csv.writer(file).writerows(seats)

        cursor.execute("UPDATE bookings SET status = 'Cancelled' WHERE pnr = %s", (pnr,))
        db.commit()
        show_output("BOOKING CANCELLED", [f"Booking {pnr} has been cancelled."])
        messagebox.showinfo("Success", "Booking cancelled successfully")
    except Exception as error:
        if db:
            db.rollback()
        messagebox.showerror("Database Error", str(error))
    finally:
        if cursor:
            cursor.close()
        if db:
            db.close()


def clear_output():
    result.delete("1.0", tk.END)
    result.insert(tk.END, "Output cleared. Select an operation to continue.")


def exit_program():
    if messagebox.askyesno("Exit", "Do you want to close the application?"):
        window.destroy()


# Main window
window = tk.Tk()
window.title("Flight Reservation System")
window.geometry("1050x950")
window.minsize(900, 750)
window.configure(bg="#F1F5F9")

header = tk.Frame(window, bg="#172554", height=85)
header.pack(fill="x")
header.pack_propagate(False)
tk.Label(header, text="✈ FLIGHT RESERVATION SYSTEM", font=("Arial", 22, "bold"),
         bg="#172554", fg="white").pack(pady=(13, 2))
tk.Label(header, text="Manage customers, flights and bookings", font=("Arial", 10),
         bg="#172554", fg="#BFDBFE").pack()

content = tk.Frame(window, bg="#F1F5F9")
content.pack(fill="both", expand=True, padx=20, pady=10)

# Customer section
customer_frame = tk.LabelFrame(content, text=" Customer Management ", font=("Arial", 11, "bold"),
                                bg="white", fg="#1E3A8A", padx=10, pady=7)
customer_frame.pack(fill="x", pady=4)
tk.Label(customer_frame, text="Name", bg="white").grid(row=0, column=0, padx=5, pady=4)
input_name = tk.Entry(customer_frame, width=20, font=("Arial", 10))
input_name.grid(row=0, column=1, padx=5, pady=4)
tk.Label(customer_frame, text="Age", bg="white").grid(row=0, column=2, padx=5, pady=4)
input_age = tk.Entry(customer_frame, width=8, font=("Arial", 10))
input_age.grid(row=0, column=3, padx=5, pady=4)
tk.Label(customer_frame, text="Phone", bg="white").grid(row=0, column=4, padx=5, pady=4)
input_phone = tk.Entry(customer_frame, width=16, font=("Arial", 10))
input_phone.grid(row=0, column=5, padx=5, pady=4)
tk.Button(customer_frame, text="Add Customer", command=add_customer, bg="#2563EB", fg="white", relief="flat").grid(row=1, column=1, padx=5, pady=5)
tk.Button(customer_frame, text="View Customers", command=view_customers, bg="#0F766E", fg="white", relief="flat").grid(row=1, column=2, padx=5, pady=5)

# Flight section
flight_frame = tk.LabelFrame(content, text=" Flight Management ", font=("Arial", 11, "bold"),
                             bg="white", fg="#1E3A8A", padx=10, pady=7)
flight_frame.pack(fill="x", pady=4)
for text, row, col in [("Flight No.", 0, 0), ("Source", 0, 2), ("Destination", 0, 4), ("Date (YYYY-MM-DD)", 1, 0), ("Fare (Rs.)", 1, 2)]:
    tk.Label(flight_frame, text=text, bg="white").grid(row=row, column=col, padx=5, pady=4, sticky="w")
input_flight = tk.Entry(flight_frame, width=14, font=("Arial", 10)); input_flight.grid(row=0, column=1, padx=5, pady=4)
input_source = tk.Entry(flight_frame, width=14, font=("Arial", 10)); input_source.grid(row=0, column=3, padx=5, pady=4)
input_destination = tk.Entry(flight_frame, width=14, font=("Arial", 10)); input_destination.grid(row=0, column=5, padx=5, pady=4)
input_date = tk.Entry(flight_frame, width=14, font=("Arial", 10)); input_date.grid(row=1, column=1, padx=5, pady=4)
input_fare = tk.Entry(flight_frame, width=14, font=("Arial", 10)); input_fare.grid(row=1, column=3, padx=5, pady=4)
tk.Button(flight_frame, text="Add Flight", command=add_flight, bg="#2563EB", fg="white", relief="flat").grid(row=2, column=1, padx=5, pady=5)
tk.Button(flight_frame, text="View Flights", command=view_flights, bg="#0F766E", fg="white", relief="flat").grid(row=2, column=2, padx=5, pady=5)

# Ticket booking section
ticket_frame = tk.LabelFrame(content, text=" Book Ticket ", font=("Arial", 11, "bold"),
                             bg="white", fg="#1E3A8A", padx=10, pady=7)
ticket_frame.pack(fill="x", pady=4)
tk.Label(ticket_frame, text="Customer ID", bg="white").grid(row=0, column=0, padx=5, pady=4)
input_customer_id = tk.Entry(ticket_frame, width=13, font=("Arial", 10)); input_customer_id.grid(row=0, column=1, padx=5, pady=4)
tk.Label(ticket_frame, text="Flight Number", bg="white").grid(row=0, column=2, padx=5, pady=4)
input_booking_flight = tk.Entry(ticket_frame, width=13, font=("Arial", 10)); input_booking_flight.grid(row=0, column=3, padx=5, pady=4)
tk.Label(ticket_frame, text="Seat (e.g. 1A)", bg="white").grid(row=0, column=4, padx=5, pady=4)
input_seat_no = tk.Entry(ticket_frame, width=12, font=("Arial", 10)); input_seat_no.grid(row=0, column=5, padx=5, pady=4)
tk.Button(ticket_frame, text="Show Seat Layout", command=show_seat_layout, bg="#0F766E", fg="white", relief="flat", padx=10).grid(row=1, column=1, columnspan=2, pady=6)
tk.Button(ticket_frame, text="Book Ticket", command=book_ticket, bg="#7C3AED", fg="white", relief="flat", padx=12).grid(row=1, column=3, columnspan=2, pady=6)

# Booking section
booking_frame = tk.LabelFrame(content, text=" Booking Management ", font=("Arial", 11, "bold"),
                               bg="white", fg="#1E3A8A", padx=10, pady=7)
booking_frame.pack(fill="x", pady=4)
tk.Label(booking_frame, text="Enter PNR", bg="white").pack(side="left", padx=8, pady=5)
input_pnr = tk.Entry(booking_frame, width=18, font=("Arial", 10)); input_pnr.pack(side="left", padx=5, pady=5)
tk.Button(booking_frame, text="View Booking", command=view_booking, bg="#2563EB", fg="white", relief="flat").pack(side="left", padx=5)
tk.Button(booking_frame, text="Cancel Booking", command=cancel_booking, bg="#DC2626", fg="white", relief="flat").pack(side="left", padx=5)

# Output section
output_heading = tk.Frame(content, bg="#172554")
output_heading.pack(fill="x", pady=(7, 0))
tk.Label(output_heading, text="  SYSTEM OUTPUT", font=("Arial", 12, "bold"), bg="#172554", fg="white", pady=9).pack(side="left")
tk.Button(output_heading, text="Clear Output", command=clear_output, bg="#334155", fg="white", relief="flat").pack(side="right", padx=10, pady=5)
output_frame = tk.Frame(content, bg="#CBD5E1", padx=2, pady=2)
output_frame.pack(fill="both", expand=True, pady=(0, 5))
scrollbar = tk.Scrollbar(output_frame); scrollbar.pack(side="right", fill="y")
result = tk.Text(output_frame, height=9, font=("Consolas", 11), bg="#F8FAFC", fg="#1E293B",
                 insertbackground="#1E293B", relief="flat", padx=12, pady=12, wrap="word",
                 yscrollcommand=scrollbar.set)
result.pack(side="left", fill="both", expand=True)
scrollbar.config(command=result.yview)
result.insert(tk.END, "Welcome to the Flight Reservation System!\n\nAdd or view customers and flights, book a ticket, or manage an existing booking.")

footer = tk.Frame(window, bg="#172554")
footer.pack(fill="x", side="bottom")
tk.Button(footer, text="Exit Application", command=exit_program, bg="#DC2626", fg="white",
          font=("Arial", 10, "bold"), relief="flat", padx=15, pady=5).pack(pady=6)

window.mainloop()
