# Library Management System API

This project is a backend REST API for a Library Management System developed using Django and Django Rest Framework. The API provides endpoints for managing student data, borrowed books, and handling book borrowings.

## Features

- **Student Data Management:** CRUD operations for managing student information.
- **Borrowed Books:** Tracks borrowed books, return dates, and fine amounts.
- **Book Borrowing:** Ability to borrow books, calculating due dates, and handling fines.

## Authentication

The current version lacks authentication, and it is recommended to implement proper authentication mechanisms before deploying in a production environment.

## Getting Started

1. Clone the repository:

bash
'git clone https://github.com/coder30427/library-management-api.git'
'cd library-management-api'

Install dependencies:
'pip install -r requirements.txt'

Run migrations:
'python manage.py migrate'

Start the development server:
'python manage.py runserver'


The API will be accessible at http://127.0.0.1:8000/api/


