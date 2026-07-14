# Console Bank Backend

## Overview

This project is the backend portion of a simple banking application built with Python. It follows a layered architecture using Models, Services, and Repositories, and supports both MySQL and MongoDB for data storage.

## Features

- Create a bank account
- Retrieve account information
- Deposit money
- Withdraw money
- View transaction history
- Prevent overdrafts
- Record deposits and withdrawals
- Unit tested with Pytest

## Technologies

- Python 3
- MySQL
- MongoDB
- Pytest
- mysql-connector-python
- PyMongo

## Project Structure

```text
ConsoleBankBackend/
├── Models/
├── MongoRepositories/
├── MySQLRepositories/
├── Services/
├── tests/
├── mongo_db.py
├── mysql_db.py
├── requirements.txt
└── README.md
```

## Architecture

```text
Service Layer
      ↓
Repository Layer
      ↓
MySQL / MongoDB
```

## Running the Project

Install dependencies:

```bash
pip install -r requirements.txt
```

Run all tests:

```bash
python -m pytest -v
```

## Tests

The project includes unit tests for:

- MongoDB Account Service
- MySQL Account Service
- Backend database functionality
