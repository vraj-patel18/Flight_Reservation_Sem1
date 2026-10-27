from database import connect_db


from database import connect_db

def add_customer():
    name = input("Customer name: ")
    age = int(input("Age: "))
    phone = input("Phone: ")

    db = connect_db()
    cursor = db.cursor()

    cursor.execute(
        "INSERT INTO customers (name, age, phone) VALUES (%s, %s, %s)",
        (name, age, phone)
    )

    db.commit()

    print("Customer added successfully!")
    print("Customer ID:", cursor.lastrowid)

    cursor.close()
    db.close()

def view_customers():
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("SELECT * FROM customers")
    customers = cursor.fetchall()
    if not customers:
        print("No customers found.")
    for customer in customers:
        print(customer)
    cursor.close()
    db.close()

def update_customer():
    customer_id = int(input("Customer ID: "))
    name = input("New name: ")
    age = int(input("New age: "))
    phone = input("New phone: ")
    db = connect_db()
    cursor = db.cursor()
    cursor.execute("UPDATE customers SET name=%s, age=%s, phone=%s WHERE id=%s", (name, age, phone, customer_id))
    db.commit()
    print("Customer updated." if cursor.rowcount else "Customer not found.")
    cursor.close()
    db.close()
