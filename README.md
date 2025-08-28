# FastAPI Authentication Service

This is a standalone authentication microservice built with FastAPI. It provides user registration, token-based login (JWT), and a protected endpoint to retrieve user data.

## Features

- **User Registration**: Create new users with a unique email and password.
- **JWT Authentication**: Securely log in to get a JSON Web Token (JWT) using the **RS256** algorithm.
- **Password Hashing**: Passwords are securely hashed using Passlib (bcrypt).
- **Docker Support**: Includes a `Dockerfile` and `docker-compose.yml` for a complete, orchestrated setup.
- **Configuration Management**: All configuration is managed via environment variables (`.env` file).
- **PostgreSQL Database**: Uses a robust PostgreSQL database.
- **Testing**: Comes with a `pytest` suite configured to run against a test database.

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
- OpenSSL (for generating keys)

### 1. Generate RSA Keys

The service uses the RS256 algorithm for JWTs, which requires a private and public key pair.

First, create a directory to store them:
```bash
mkdir keys
```

Now, generate the private and public keys using OpenSSL:
```bash
# Generate a 2048-bit private key
openssl genpkey -algorithm RSA -out keys/private.pem -pkeyopt rsa_keygen_bits:2048

# Extract the public key from the private key
openssl rsa -pubout -in keys/private.pem -out keys/public.pem
```

### 2. Configure Your Environment

Create a `.env` file for your configuration. You can copy the structure from the non-existent `.env.example` or create it from scratch. It must contain the following variables:

```
# .env
DATABASE_URL="postgresql://user:password@db:5432/auth_db"
TEST_DATABASE_URL="sqlite:///./test.db"

# Paths to the generated RSA keys
PRIVATE_KEY_PATH="keys/private.pem"
PUBLIC_KEY_PATH="keys/public.pem"
```
The default values for the database are configured to work with `docker-compose` out of the box.

### 3. Build and Run the Services

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

The tests are configured to run against an in-memory SQLite database by default.

From your local machine (with a virtual environment activated and dependencies installed), run the tests:
```bash
pytest
```

---

## Manual Local Setup (Without Docker)

If you prefer not to use Docker, you can run the application locally.

1.  **Set up a virtual environment** and install dependencies:
    ```bash
    python -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt
    ```
2.  **Generate RSA Keys** as described in the Docker setup section.
3.  **Ensure a database is running** on your local machine (e.g., PostgreSQL).
4.  **Create your `.env` file** as described in the Docker setup.
5.  **Update `.env`**:
    - If using PostgreSQL, change `DATABASE_URL` to point to your local instance (e.g., `postgresql://user:pass@localhost:5432/dbname`).
6.  **Run the application**:
    ```bash
    uvicorn app.main:app --reload
    ```
