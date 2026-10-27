from customer import add_customer, view_customers, update_customer
from flight import add_flight, view_flights, search_flight
from booking import book_seat, view_booking, cancel_booking
from booking import booking_history, view_seat_matrix

while True:
    print("\n--- FLIGHT RESERVATION SYSTEM ---")
    print("1. Add Customer")
    print("2. View Customers")
    print("3. Update Customer")
    print("4. Add Flight")
    print("5. View Flights")
    print("6. Search Flight")
    print("7. Book Seat")
    print("8. View Booking")
    print("9. Cancel Booking")
    print("10. Booking History")
    print("11. View Seat Matrix")
    print("12. Exit")
    choice = input("Enter choice: ")

    if choice == "1":
        add_customer()
    elif choice == "2":
        view_customers()
    elif choice == "3":
        update_customer()
    elif choice == "4":
        add_flight()
    elif choice == "5":
        view_flights()
    elif choice == "6":
        search_flight()
    elif choice == "7":
        book_seat()
    elif choice == "8":
        view_booking()
    elif choice == "9":
        cancel_booking()
    elif choice == "10":
        booking_history()
    elif choice == "11":
        view_seat_matrix()
    elif choice == "12":
        print("Thank you for using the system.")
        break
    else:
        print("Invalid choice.")
