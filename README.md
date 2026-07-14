# Console Bank Backend

## Overview

This project is a backend banking system developed using Python and MySQL following the MVC architecture. The application provides the business logic and database access for a simple banking system.

## Features

- Create a bank account
- Retrieve account information
- Deposit money
- Withdraw money
- View transaction history

## Technologies Used

- Python 3
- MySQL
- mysql-connector-python

## Project Structure


ConsoleBankBackend/
│
├── Models/
├── Repositories/
├── Services/
├── db.py
├── requirements.txt
└── README.md


## Architecture


Service
   ↓
Repository
   ↓
MySQL Database


## Database

**Schema Name**

cognixia_bank

**Tables**

- users
- accounts
- transactions

## Running the Application

1. Start the MySQL server.
2. Ensure the `cognixia_bank` database and tables exist.
3. Install the required dependency:

pip install -r requirements.txt


4. Run your backend tests (for example, `test_backend.py`) to verify the service and repository layers are communicating with the database.
