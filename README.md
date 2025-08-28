# FastAPI Authentication Service

This is a standalone authentication microservice built with FastAPI. It provides user registration, token-based login (JWT), and a protected endpoint to retrieve user data.

## Features

- **User Registration**: Create new users with a unique email and password.
- **JWT Authentication**: Securely log in to get a JSON Web Token (JWT).
- **Password Hashing**: Passwords are securely hashed using Passlib (bcrypt).
- **Docker Support**: Includes a `Dockerfile` and `docker-compose.yml` for a complete, orchestrated setup.
- **Configuration Management**: All configuration is managed via environment variables (`.env` file).
- **PostgreSQL Database**: Uses a robust PostgreSQL database.
- **Testing**: Comes with a `pytest` suite configured to run against a test PostgreSQL database.

## Tech Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: [PostgreSQL](https://www.postgresql.org/) with [SQLModel](https://sqlmodel.tiangolo.com/)
- **Configuration**: [Pydantic-Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **Authentication**: [Passlib](https://passlib.readthedocs.io/en/stable/) & [python-jose](https://github.com/mpdavis/python-jose)

---

## Getting Started with Docker (Recommended)

This is the easiest way to get the service and its database up and running.

### Prerequisites

- Docker and Docker Compose

### 1. Configure Your Environment

First, create a `.env` file from the provided example:
```bash
cp .env.example .env
```

Now, open the `.env` file and change the `SECRET_KEY` to a new, random value. You can generate one with:
```bash
openssl rand -hex 32
```
The other default values for the database are configured to work with `docker-compose` out of the box.

### 2. Build and Run the Services

Use Docker Compose to build the API image and start both the API and the database containers:
```bash
docker-compose up --build
```
The API will be available at `http://127.0.0.1:8000`.

---

## API Documentation

Once the service is running, interactive API documentation (Swagger UI) is available at:
[http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

---

## Running Tests

The tests are designed to run against a separate test database, as defined by the `TEST_DATABASE_URL` in your `.env` file.

### 1. Ensure Services are Running

Make sure the database container is running via Docker Compose:
```bash
docker-compose up -d db
```

### 2. Run Pytest

From your local machine (with a virtual environment activated and dependencies installed), run the tests:
```bash
# Make sure you have a .env file with the correct TEST_DATABASE_URL
pytest
```
The `PYTHONPATH=.` is no longer needed if you install your project in editable mode (`pip install -e .`), but is included here for robustness.

---

## Manual Local Setup (Without Docker)

If you prefer not to use Docker, you can run the application locally.

1.  **Set up a virtual environment** and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Ensure PostgreSQL is running** on your local machine.
3.  **Create your `.env` file** as described in the Docker setup.
4.  **Update `.env`**:
    - Change `DATABASE_URL` and `TEST_DATABASE_URL` to point to your local PostgreSQL instance (e.g., `postgresql://user:pass@localhost:5432/dbname`).
    - Make sure you have created the two databases (`auth_db` and `test_auth_db`) in PostgreSQL.
5.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```
