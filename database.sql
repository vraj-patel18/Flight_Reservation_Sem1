CREATE DATABASE IF NOT EXISTS flight_reservation;
USE flight_reservation;

CREATE TABLE IF NOT EXISTS customers (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    phone VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS flights (
    id INT AUTO_INCREMENT PRIMARY KEY,
    flight_no VARCHAR(20) UNIQUE,
    source VARCHAR(50),
    destination VARCHAR(50),
    flight_date DATE,
    fare DECIMAL(10,2),
    seat_file VARCHAR(100)
);

CREATE TABLE IF NOT EXISTS bookings (
    pnr INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    flight_id INT,
    seat_no VARCHAR(10),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (flight_id) REFERENCES flights(id)
);

USE flight_reservation;

CREATE TABLE IF NOT EXISTS bookings (
    pnr INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT,
    flight_id INT,
    seat_no VARCHAR(10),
    status VARCHAR(20),
    FOREIGN KEY (customer_id) REFERENCES customers(id),
    FOREIGN KEY (flight_id) REFERENCES flights(id)
);