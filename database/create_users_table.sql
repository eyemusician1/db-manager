-- Database schema for user authentication system
-- Run this script to create the users table in your database

-- Create database if it doesn't exist
CREATE DATABASE IF NOT EXISTS backmeup_system;
USE backmeup_system;

-- Create users table for login/registration
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    full_name VARCHAR(100),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP NULL,
    is_active BOOLEAN DEFAULT TRUE,
    role VARCHAR(20) DEFAULT 'user',
    INDEX idx_username (username),
    INDEX idx_email (email),
    INDEX idx_is_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Insert default admin user (password: admin123)
-- Note: In production, use proper password hashing (bcrypt, argon2, etc.)
INSERT INTO users (username, email, password, full_name, role, is_active)
VALUES ('admin', 'admin@backmeup.com', 'admin123', 'System Administrator', 'admin', TRUE)
ON DUPLICATE KEY UPDATE username=username;

-- Create index for faster lookups
CREATE INDEX idx_users_active ON users(is_active, username);

