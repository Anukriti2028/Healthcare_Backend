
# Healthcare Backend API

A healthcare management backend built with Django REST Framework and PostgreSQL.

## Features

- User registration and JWT authentication
- Patient management APIs
- Doctor management APIs
- Patient-doctor mapping APIs
- Protected endpoints

## Tech Stack

- Python
- Django
- Django REST Framework
- PostgreSQL
- Simple JWT
- Postman

## Setup Instructions
Clone this repository.
Create and activate a Python virtual environment.
Install dependencies:

   `pip install -r requirements.txt`

Create a `.env` file using the environment variables below.
Create a PostgreSQL database named `healthcare_db`.
Apply migrations:

   `python manage.py migrate`

Start the development server:

   `python manage.py runserver`

## Environment Variables

Configure these variables in your private `.env` file:

- `SECRET_KEY`
- `DEBUG`
- `DB_NAME`
- `DB_USER`
- `DB_PASSWORD`
- `DB_HOST`
- `DB_PORT`

Never commit `.env` or real credentials to GitHub.

## API Endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| POST | `/api/auth/register/` | Register a user |
| POST | `/api/auth/login/` | Obtain JWT tokens |
| GET, POST | `/api/patients/` | List and create patients |
| GET, POST | `/api/doctors/` | List and create doctors |
| POST | `/api/mappings/` | Assign a doctor to a patient |
| GET | `/api/mappings/` | List mappings |
| GET | `/api/mappings/<patient_id>/` | View a patient's doctors |
| DELETE | `/api/mappings/<id>/` | Delete a mapping |
