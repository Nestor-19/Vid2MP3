-- Create database user
CREATE USER 'auth_user'@'localhost' IDENTIFIED BY 'Auth123';

-- Create Database
CREATE DATABASE auth;

-- Grant access to database for the created user
GRANT ALL PRIVILEGES ON auth.* TO 'auth_user'@'localhost';

USE auth;

-- Create user table in database
CREATE TABLE user (
    id INT NOT NULL AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

-- Insert user into user table
-- This user will have access to the Gateway API
INSERT INTO user (email, password) VALUES ('admin@gmail.com', 'admin123');