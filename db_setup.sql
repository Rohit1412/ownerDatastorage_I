-- db_setup.sql
CREATE DATABASE owner_db;

USE owner_db;

CREATE TABLE IF NOT EXISTS owners (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100),
    age INT,
    gender VARCHAR(10),
    restaurant_name VARCHAR(100)
);

