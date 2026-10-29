FLIGHT RESERVATION SYSTEM 

This is the Repository of the project based mainly on Python in my first Semester of B.Tech. It consists of 3 members: Vraj(me), Suyash and Pranjal

This Project consists of all the files we made for our flight booking/reservation system, which uses Python, MySQL and CSV file systems along with some other Python Libraries.


FILES
- main.py: menu
- database.py: MySQL connection
- customer.py: customer options
- flight.py: flight options
- seat.py: CSV seat matrix functions
- booking.py: booking, viewing, cancellation, history
- database.sql: creates the MySQL database and tables
- seat_matrices/: one CSV file per flight is created here
- gui.py: contains tkinter code for basic frontend 

SETUP
1. Run database.sql in MySQL Workbench.
2. Install the connector: pip install mysql-connector-python
3. In database.py, replace YOUR_PASSWORD with your MySQL password.
4. Open a terminal in this folder and run: python main.py

DATES must be entered as YYYY-MM-DD, for example 2026-11-15.
Seat names look like 2B. Choose 4 or 6 seats per row.

MySQL stores customer, flight and booking data. CSV stores only seat matrices.
This is a simple learning project. Test it with sample data first.
