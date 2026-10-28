
import tkinter as tk
from tkinter import messagebox
from database import connect_db


# Add customer
def add_customer():
    name = input_name.get().strip()
    age = input_age.get().strip()
    phone = input_phone.get().strip()

    if name == "" or age == "" or phone == "":
        messagebox.showerror("Error", "Please enter all customer details")
        return

    try:
        age = int(age)

        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            "INSERT INTO customers (name, age, phone) VALUES (%s, %s, %s)",
            (name, age, phone)
        )

        db.commit()
        messagebox.showinfo("Success", "Customer added successfully!")

        input_name.delete(0, tk.END)
        input_age.delete(0, tk.END)
        input_phone.delete(0, tk.END)

        cursor.close()
        db.close()

    except ValueError:
        messagebox.showerror("Error", "Age must be a number")

    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# View customers
def view_customers():
    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM customers")
        data = cursor.fetchall()

        result.delete("1.0", tk.END)
        result.insert(tk.END, "CUSTOMER DETAILS\n")
        result.insert(tk.END, "-" * 70 + "\n\n")

        if len(data) == 0:
            result.insert(tk.END, "No customers found.")
        else:
            for row in data:
                result.insert(tk.END, f"ID: {row[0]}\n")
                result.insert(tk.END, f"Name: {row[1]}\n")
                result.insert(tk.END, f"Age: {row[2]}\n")
                result.insert(tk.END, f"Phone: {row[3]}\n")
                result.insert(tk.END, "-" * 70 + "\n")

        cursor.close()
        db.close()

    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# Add flight
def add_flight():
    flight_no = input_flight.get().strip().upper()
    source = input_source.get().strip()
    destination = input_destination.get().strip()
    date = input_date.get().strip()
    fare = input_fare.get().strip()

    if (flight_no == "" or source == "" or destination == ""
            or date == "" or fare == ""):
        messagebox.showerror("Error", "Please enter all flight details")
        return

    try:
        fare = float(fare)

        if fare < 0:
            messagebox.showerror("Error", "Fare cannot be negative")
            return

        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            """INSERT INTO flights
            (flight_no, source, destination, flight_date, fare, seat_file)
            VALUES (%s, %s, %s, %s, %s, %s)""",
            (flight_no, source, destination, date, fare, flight_no + ".csv")
        )

        db.commit()
        messagebox.showinfo("Success", "Flight added successfully!")

        input_flight.delete(0, tk.END)
        input_source.delete(0, tk.END)
        input_destination.delete(0, tk.END)
        input_date.delete(0, tk.END)
        input_fare.delete(0, tk.END)

        cursor.close()
        db.close()

    except ValueError:
        messagebox.showerror("Error", "Enter a valid fare")

    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# View flights
def view_flights():
    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute("SELECT * FROM flights")
        data = cursor.fetchall()

        result.delete("1.0", tk.END)
        result.insert(tk.END, "FLIGHT DETAILS\n")
        result.insert(tk.END, "-" * 70 + "\n\n")

        if len(data) == 0:
            result.insert(tk.END, "No flights found.")
        else:
            for row in data:
                result.insert(tk.END, f"Flight ID: {row[0]}\n")
                result.insert(tk.END, f"Flight Number: {row[1]}\n")
                result.insert(tk.END, f"Source: {row[2]}\n")
                result.insert(tk.END, f"Destination: {row[3]}\n")
                result.insert(tk.END, f"Date: {row[4]}\n")
                result.insert(tk.END, f"Fare: Rs. {row[5]}\n")
                result.insert(tk.END, "-" * 70 + "\n")

        cursor.close()
        db.close()

    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# View booking
def view_booking():
    pnr = input_pnr.get().strip().upper()

    if pnr == "":
        messagebox.showerror("Error", "Please enter the PNR")
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            """SELECT bookings.pnr, customers.name,
            flights.flight_no, flights.source, flights.destination,
            bookings.seat_no, bookings.status
            FROM bookings
            JOIN customers ON bookings.customer_id = customers.id
            JOIN flights ON bookings.flight_id = flights.id
            WHERE bookings.pnr = %s""",
            (pnr,)
        )

        data = cursor.fetchone()

        result.delete("1.0", tk.END)
        result.insert(tk.END, "BOOKING DETAILS\n")
        result.insert(tk.END, "-" * 70 + "\n\n")

        if data:
            result.insert(tk.END, f"PNR: {data[0]}\n")
            result.insert(tk.END, f"Customer: {data[1]}\n")
            result.insert(tk.END, f"Flight: {data[2]}\n")
            result.insert(tk.END, f"From: {data[3]}\n")
            result.insert(tk.END, f"To: {data[4]}\n")
            result.insert(tk.END, f"Seat Number: {data[5]}\n")
            result.insert(tk.END, f"Status: {data[6]}\n")
        else:
            result.insert(tk.END, "Booking not found.")

        cursor.close()
        db.close()

    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# Cancel booking
def cancel_booking():
    pnr = input_pnr.get().strip().upper()

    if pnr == "":
        messagebox.showerror("Error", "Please enter the PNR")
        return

    try:
        db = connect_db()
        cursor = db.cursor()

        cursor.execute(
            """UPDATE bookings
            SET status = 'Cancelled'
            WHERE pnr = %s AND status = 'Confirmed'""",
            (pnr,)
        )

        db.commit()

        if cursor.rowcount > 0:
            messagebox.showinfo("Success", "Booking cancelled successfully!")
            result.delete("1.0", tk.END)
            result.insert(tk.END, f"Booking {pnr} has been cancelled.")
        else:
            messagebox.showerror(
                "Error",
                "Booking not found or already cancelled"
            )

        cursor.close()
        db.close()

    except Exception as error:
        messagebox.showerror("Database Error", str(error))


# Clear output
def clear_output():
    result.delete("1.0", tk.END)
    result.insert(tk.END, "Output cleared. Select an operation to continue.")


# Exit application
def exit_program():
    if messagebox.askyesno("Exit", "Do you want to close the application?"):
        window.destroy()


# Main window
window = tk.Tk()
window.title("Flight Reservation System")
window.geometry("1000x900")
window.minsize(850, 700)
window.configure(bg="#F1F5F9")


# Header
header = tk.Frame(window, bg="#172554", height=90)
header.pack(fill="x")
header.pack_propagate(False)

tk.Label(
    header,
    text="✈ FLIGHT RESERVATION SYSTEM",
    font=("Arial", 22, "bold"),
    bg="#172554",
    fg="white"
).pack(pady=(15, 2))

tk.Label(
    header,
    text="Manage customers, flights and bookings",
    font=("Arial", 10),
    bg="#172554",
    fg="#BFDBFE"
).pack()


# Main content
content = tk.Frame(window, bg="#F1F5F9")
content.pack(fill="both", expand=True, padx=20, pady=15)


# Customer section
customer_frame = tk.LabelFrame(
    content,
    text=" Customer Management ",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1E3A8A",
    padx=12,
    pady=10
)
customer_frame.pack(fill="x", pady=5)

tk.Label(customer_frame, text="Name", bg="white").grid(
    row=0, column=0, sticky="w", padx=5, pady=5
)
input_name = tk.Entry(customer_frame, width=22, font=("Arial", 10))
input_name.grid(row=0, column=1, padx=5, pady=5)

tk.Label(customer_frame, text="Age", bg="white").grid(
    row=0, column=2, sticky="w", padx=5, pady=5
)
input_age = tk.Entry(customer_frame, width=10, font=("Arial", 10))
input_age.grid(row=0, column=3, padx=5, pady=5)

tk.Label(customer_frame, text="Phone", bg="white").grid(
    row=0, column=4, sticky="w", padx=5, pady=5
)
input_phone = tk.Entry(customer_frame, width=18, font=("Arial", 10))
input_phone.grid(row=0, column=5, padx=5, pady=5)

tk.Button(
    customer_frame,
    text="Add Customer",
    command=add_customer,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=10
).grid(row=1, column=1, padx=5, pady=8)

tk.Button(
    customer_frame,
    text="View Customers",
    command=view_customers,
    bg="#0F766E",
    fg="white",
    activebackground="#115E59",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=10
).grid(row=1, column=2, padx=5, pady=8)


# Flight section
flight_frame = tk.LabelFrame(
    content,
    text=" Flight Management ",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1E3A8A",
    padx=12,
    pady=10
)
flight_frame.pack(fill="x", pady=5)

tk.Label(flight_frame, text="Flight No.", bg="white").grid(
    row=0, column=0, sticky="w", padx=5, pady=5
)
input_flight = tk.Entry(flight_frame, width=15, font=("Arial", 10))
input_flight.grid(row=0, column=1, padx=5, pady=5)

tk.Label(flight_frame, text="Source", bg="white").grid(
    row=0, column=2, sticky="w", padx=5, pady=5
)
input_source = tk.Entry(flight_frame, width=15, font=("Arial", 10))
input_source.grid(row=0, column=3, padx=5, pady=5)

tk.Label(flight_frame, text="Destination", bg="white").grid(
    row=0, column=4, sticky="w", padx=5, pady=5
)
input_destination = tk.Entry(flight_frame, width=15, font=("Arial", 10))
input_destination.grid(row=0, column=5, padx=5, pady=5)

tk.Label(flight_frame, text="Date (YYYY-MM-DD)", bg="white").grid(
    row=1, column=0, sticky="w", padx=5, pady=5
)
input_date = tk.Entry(flight_frame, width=15, font=("Arial", 10))
input_date.grid(row=1, column=1, padx=5, pady=5)

tk.Label(flight_frame, text="Fare (Rs.)", bg="white").grid(
    row=1, column=2, sticky="w", padx=5, pady=5
)
input_fare = tk.Entry(flight_frame, width=15, font=("Arial", 10))
input_fare.grid(row=1, column=3, padx=5, pady=5)

tk.Button(
    flight_frame,
    text="Add Flight",
    command=add_flight,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=10
).grid(row=2, column=1, padx=5, pady=8)

tk.Button(
    flight_frame,
    text="View Flights",
    command=view_flights,
    bg="#0F766E",
    fg="white",
    activebackground="#115E59",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=10
).grid(row=2, column=2, padx=5, pady=8)


# Booking section
booking_frame = tk.LabelFrame(
    content,
    text=" Booking Management ",
    font=("Arial", 11, "bold"),
    bg="white",
    fg="#1E3A8A",
    padx=12,
    pady=10
)
booking_frame.pack(fill="x", pady=5)

tk.Label(booking_frame, text="Enter PNR", bg="white").pack(
    side="left", padx=10, pady=5
)

input_pnr = tk.Entry(booking_frame, width=20, font=("Arial", 10))
input_pnr.pack(side="left", padx=5, pady=5)

tk.Button(
    booking_frame,
    text="View Booking",
    command=view_booking,
    bg="#2563EB",
    fg="white",
    activebackground="#1D4ED8",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=10
).pack(side="left", padx=5)

tk.Button(
    booking_frame,
    text="Cancel Booking",
    command=cancel_booking,
    bg="#DC2626",
    fg="white",
    activebackground="#B91C1C",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=10
).pack(side="left", padx=5)


# Output heading
output_heading = tk.Frame(content, bg="#172554")
output_heading.pack(fill="x", pady=(12, 0))

tk.Label(
    output_heading,
    text="  SYSTEM OUTPUT",
    font=("Arial", 12, "bold"),
    bg="#172554",
    fg="white",
    pady=10
).pack(side="left")

tk.Button(
    output_heading,
    text="Clear Output",
    command=clear_output,
    bg="#334155",
    fg="white",
    relief="flat",
    font=("Arial", 9, "bold"),
    padx=10
).pack(side="right", padx=10, pady=5)


# Output area with scrollbar
output_frame = tk.Frame(content, bg="#CBD5E1", padx=2, pady=2)
output_frame.pack(fill="both", expand=True, pady=(0, 8))

scrollbar = tk.Scrollbar(output_frame)
scrollbar.pack(side="right", fill="y")

result = tk.Text(
    output_frame,
    height=12,
    font=("Consolas", 11),
    bg="#F8FAFC",
    fg="#1E293B",
    insertbackground="#1E293B",
    relief="flat",
    padx=12,
    pady=12,
    wrap="word",
    yscrollcommand=scrollbar.set
)
result.pack(side="left", fill="both", expand=True)

scrollbar.config(command=result.yview)

result.insert(
    tk.END,
    "Welcome to the Flight Reservation System!\n\n"
    "Choose an operation above to get started.\n"
    "Customer and flight records will appear here."
)


# Footer
footer = tk.Frame(window, bg="#172554")
footer.pack(fill="x", side="bottom")

tk.Button(
    footer,
    text="Exit Application",
    command=exit_program,
    bg="#DC2626",
    fg="white",
    activebackground="#B91C1C",
    font=("Arial", 10, "bold"),
    relief="flat",
    padx=15,
    pady=5
).pack(pady=8)


# Run application
window.mainloop()