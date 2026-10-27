USE flight_reservation;

-- Sample flight records matching the CSV seat matrices in seat_matrices/
-- Run this after creating the database tables.
INSERT INTO flights (flight_no, source, destination, flight_date, fare, seat_file) VALUES
('AI101', 'Chennai', 'Delhi', '2026-11-05', 5200.00, 'AI101.csv'),
('6E205', 'Chennai', 'Bengaluru', '2026-11-06', 2400.00, '6E205.csv'),
('UK310', 'Delhi', 'Mumbai', '2026-11-07', 6100.00, 'UK310.csv'),
('SG412', 'Hyderabad', 'Chennai', '2026-11-08', 3200.00, 'SG412.csv'),
('AI550', 'Mumbai', 'Kolkata', '2026-11-09', 5800.00, 'AI550.csv'),
('6E777', 'Bengaluru', 'Hyderabad', '2026-11-10', 1900.00, '6E777.csv'),
('QP123', 'Chennai', 'Pune', '2026-11-11', 3600.00, 'QP123.csv');

-- Check the inserted sample flights
SELECT * FROM flights;