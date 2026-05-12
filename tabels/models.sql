CREATE DATABASE IF NOT EXISTS financial_data;

USE financial_data;

CREATE TABLE IF NOT EXISTS store(
id INT PRIMARY KEY AUTO_INCREMENT,
store_name VARCHAR(255) NOT NULL UNIQUE,
cnpj VARCHAR(255) NOT NULL UNIQUE,
mcc_code VARCHAR (20), NOT NULL
location POINT NOT NULL SRID 4326,
SPATIAL INDEX (location)
);

CREATE TABLE IF NOT EXISTS owners(
id INT PRIMARY KEY AUTO_INCREMENT,
name VARCHAR(255) NOT NULL,
cpf VARCHAR(255) NOT NULL UNIQUE

);

CREATE TABLE IF NOT EXISTS store_owners(
owners_id INT,
store_id INT,
PRIMARY KEY(owners_id,store_id),
FOREIGN KEY (owners_id) REFERENCES owners(id) ON DELETE CASCADE,
FOREIGN KEY (store_id) REFERENCES store(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS transactions(
id INT PRIMARY KEY AUTO_INCREMENT,
transaction_value DECIMAL(19, 4) NOT NULL,
transaction_date DATETIME DEFAULT CURRENT_TIMESTAMP,
transaction_cpf VARCHAR(255) NOT NULL,
transaction_store_id INT NOT NULL,
transaction_location POINT NOT NULL SRID 4326,
SPATIAL INDEX (transaction_location),
transaction_status ENUM('PENDING','APROVED','REJECTED') DEFAULT 'PENDING',
reason TEXT default 'transaction aproved.',
FOREIGN KEY (transaction_store_id) REFERENCES store(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS blacklist(
id INT PRIMARY KEY AUTO_INCREMENT,
identifier VARCHAR(255) NOT NULL,
added_at DATETIME DEFAULT CURRENT_TIMESTAMP,
identifier_type ENUM('CPF','CNPJ') NOT NULL,
severity_level ENUM('LOW','MEDIUM','HIGH'),
reason TEXT
);

CREATE TABLE IF NOT EXISTS store_metrics (
store_id INT PRIMARY KEY,
total_chargebacks INT DEFAULT 0, 
average_ticket DECIMAL(19, 4),   
risk_level ENUM('LOW', 'MEDIUM', 'HIGH') DEFAULT 'LOW',
last_audit_date DATETIME,
FOREIGN KEY (store_id) REFERENCES store(id) ON DELETE CASCADE
);