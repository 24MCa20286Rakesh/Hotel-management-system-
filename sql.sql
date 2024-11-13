CREATE DATABASE hotel_management;
USE hotel_management;

CREATE TABLE bookings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    guest_name VARCHAR(100),
    room_number VARCHAR(20),
    nights INT,
    city VARCHAR(50),
    phone VARCHAR(20),
    email VARCHAR(100)
);
SELECT * FROM hotel_management.bookings;