# FastAPI Authentication Service

A clean, production-ready FastAPI authentication system implementing JWT (JSON Web Tokens), password hashing with Argon2 via `pwdlib`, and MySQL / PyMySQL database management using SQLAlchemy 2.0.

---

## 📁 Project Structure

```text
fastapi-auth/
├── app/
│   ├── __init__.py
│   ├── main.py                  # Application entry point & FastAPI setup
│   │
│   ├── core/                    # Core configuration and security
│   │   ├── __init__.py
│   │   ├── config.py            # Pydantic Settings & environment variables
│   │   └── security.py          # Password hashing (Argon2) & JWT utilities
│   │
│   ├── db/                      # Database setup
│   │   ├── __init__.py
│   │   ├── base.py              # SQLAlchemy 2.0 DeclarativeBase
│   │   ├── session.py           # Engine & SessionLocal provider
│   │   └── init_db.py           # Table initialization script
│   │
│   ├── models/                  # Database models
│   │   ├── __init__.py
│   │   └── user.py              # User ORM model
│   │
│   ├── schemas/                 # Pydantic validation schemas
│   │   ├── __init__.py
│   │   └── user.py              # User, Token, and Login schemas
│   │
│   ├── repositories/            # Data access layer
│   │   ├── __init__.py
│   │   └── user_repository.py   # User database queries (CRUD)
│   │
│   ├── services/                # Business logic layer
│   │   ├── __init__.py
│   │   └── auth_service.py      # Registration & authentication logic
│   │
│   ├── api/                     # HTTP API endpoints
│   │   ├── __init__.py
│   │   └── routes/
│   │       ├── __init__.py      # Route aggregation
│   │       ├── auth.py          # /register, /login, /login/token
│   │       └── users.py         # /users/me, /users
│   │
│   └── dependencies/            # FastAPI dependency injections
│       ├── __init__.py
│       └── auth.py              # JWT authentication & permission guards
│
├── .env                         # Local environment variables
├── .env.example                 # Environment variables template
├── .gitignore                   # Git ignore file
├── pyproject.toml               # Project configuration & dependencies
├── uv.lock                      # Dependency lock file
└── README.md                    # Project documentation
```

---

## 🛠️ Tech Stack & Dependencies

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/)
- **Server**: [Uvicorn](https://www.uvicorn.org/) (Standard)
- **Database ORM**: [SQLAlchemy 2.0](https://www.sqlalchemy.org/)
- **Database Driver**: [PyMySQL](https://github.com/PyMySQL/PyMySQL)
- **Configuration**: [Pydantic-Settings](https://docs.pydantic.dev/latest/concepts/pydantic_settings/)
- **Password Hashing**: [`pwdlib`](https://github.com/FrankyR/pwdlib) with **Argon2**
- **Token Management**: [PyJWT](https://pyjwt.readthedocs.io/)
- **Form Data**: `python-multipart`

---

## 🚀 Quick Start

### 1. Environment Configuration

Copy the sample environment file and adjust your database connection or secrets:

```bash
cp .env.example .env
```

Default `.env` configuration:
```env
PROJECT_NAME="FastAPI Authentication Service"
API_V1_STR="/api/v1"
DEBUG=True

# JWT Configuration
SECRET_KEY="super_secret_jwt_key_at_least_32_bytes_long_change_me_in_production"
ALGORITHM="HS256"
ACCESS_TOKEN_EXPIRE_MINUTES=30

# Database Configuration (MySQL)
DB_HOST="localhost"
DB_PORT=3306
DB_USER="root"
DB_PASSWORD=""
DB_NAME="fastapi_auth_db"
```

> **Tip**: If you prefer SQLite for quick local development without a MySQL instance, set:
> ```env
> DATABASE_URL="sqlite:///./fastapi_auth.db"
> ```

### 2. Run the Development Server

Using `uv`:

```bash
uv run uvicorn app.main:app --reload
```

Or with active virtual environment:

```bash
source .venv/bin/activate
uvicorn app.main:app --reload
```

The server will be available at:
- **API**: [http://127.0.0.1:8000](http://127.0.0.1:8000)
- **Interactive Swagger Docs**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
- **ReDoc**: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 🔐 API Endpoints

### Authentication (`/api/v1/auth`)

| Method | Endpoint | Description |
|---|---|---|
| `POST` | `/api/v1/auth/register` | Register a new user account |
| `POST` | `/api/v1/auth/login` | Authenticate using JSON (`username_or_email`, `password`) |
| `POST` | `/api/v1/auth/login/token` | Authenticate via OAuth2 form (Swagger UI "Authorize" button) |

### Users (`/api/v1/users`)

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/api/v1/users/me` | Get currently logged-in user profile |
| `PUT` | `/api/v1/users/me` | Update current user's profile or password |
| `GET` | `/api/v1/users/` | List all users (requires authentication) |
| `GET` | `/api/v1/users/{id}` | Get user by ID |
