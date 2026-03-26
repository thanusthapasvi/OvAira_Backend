CREATE DATABASE IF NOT EXISTS ovaira;
USE ovaira;

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(255) NOT NULL,
    email VARCHAR(255) NOT NULL UNIQUE,
    mobile VARCHAR(20) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    otp VARCHAR(10),
    otp_expiry DATETIME,
    reset_otp VARCHAR(10),
    reset_otp_expiry DATETIME,
    is_verified TINYINT(1) DEFAULT 0,
    gender VARCHAR(20),
    department VARCHAR(100),
    license_number VARCHAR(50),
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP
);
