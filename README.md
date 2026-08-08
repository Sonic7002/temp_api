# Educational Platform API (EduAPI)

A modern, high-performance FastAPI application providing Role-Based Access Control (RBAC) for educational interactions. The platform enables teachers to organize classrooms, upload educational notes (with PDF & MP4 media support via Supabase Storage), create quizzes, and evaluate student attempt assessments in real time.

---

## Features

- **Role-Based Access Control (RBAC)**: Enforces distinct permissions for **TEACHER** and **STUDENT** roles.
- **Classroom Management**: Teachers create and manage virtual classrooms; students explore and join classrooms.
- **Note Management**: Secure note uploads attached to classrooms with support for PDF and MP4 media streaming via Supabase Storage.
- **Quiz Generation & Editing**: Teachers generate interactive quiz questions with multiple choices and difficulty settings for specific notes.
- **Attempt Tracking**: Students initiate quiz attempts from selected classroom notes, receiving interactive questions.
- **Automated Assessment Evaluation**: Real-time answer validation and scoring recorded per student question submission.
- **Interactive Documentation**: Built-in Swagger UI and ReDoc interface for seamless API testing.

---

## Technology Stack

- **Framework**: [FastAPI](https://fastapi.tiangolo.com/) (Python 3.10+)
- **Database**: PostgreSQL (via [Neon Serverless Postgres](https://neon.tech/))
- **ORM & Drivers**: [SQLAlchemy](https://www.sqlalchemy.org/) & [psycopg](https://www.psycopg.org/)
- **File Storage**: [Supabase Storage](https://supabase.com/)
- **Authentication**: JWT tokens (via `python-jose` & `passlib[bcrypt]`)
- **Data Validation**: [Pydantic v2](https://docs.pydantic.dev/)
- **ASGI Server**: [Uvicorn](https://www.uvicorn.org/)

---

## Project Architecture

```
temp_api/
├── main.py                   # Application entrypoint & FastAPI initialization
├── README.md                 # Project documentation
├── .env                      # Environment configuration
└── app/
    ├── api/                  # API Layer
    │   ├── dependencies/     # Dependency injection (Auth, DB, RBAC, Services)
    │   │   ├── auth_deps.py
    │   │   ├── deps.py
    │   │   └── rbac.py
    │   └── v1/               # Version 1 Router & Endpoints
    │       ├── router.py     # Aggregated v1 API router
    │       ├── classrooms.py # Classroom management routes
    │       ├── notes.py      # Note upload & retrieval routes
    │       ├── quizzes.py    # Quiz creation & edit routes
    │       ├── attempts.py   # Student attempt routes
    │       └── assessments.py# Assessment answer evaluation routes
    ├── core/                 # Security & JWT configuration
    │   ├── jwt.py
    │   └── security.py
    ├── db/                   # Database session & Supabase client
    │   ├── base.py
    │   ├── session.py
    │   └── file_client.py
    ├── models/               # SQLAlchemy ORM Models
    │   ├── user.py
    │   ├── classroom.py
    │   ├── note.py
    │   ├── quiz.py
    │   ├── attempt.py
    │   └── assessment.py
    ├── repos/                # Repository Pattern (Data Access Layer)
    │   ├── user_repo.py
    │   ├── classroom_repo.py
    │   ├── note_repo.py
    │   ├── quiz_repo.py
    │   ├── attempt_repo.py
    │   └── assessment_repo.py
    ├── schemas/              # Pydantic Schemas (Request/Response validation)
    │   ├── user.py
    │   ├── classroom.py
    │   ├── note.py
    │   ├── quiz.py
    │   ├── attempt.py
    │   ├── assessment.py
    │   └── auth.py
    └── services/             # Business Logic Layer
        ├── user_service.py
        ├── classroom_service.py
        ├── notes_service.py
        ├── quiz_service.py
        ├── attempt_service.py
        └── assessment_service.py
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher installed.
- PostgreSQL database (or Neon Postgres connection URI).
- Supabase project for storage (optional, required for note media upload).

### Installation

1. **Clone the repository**:
   ```bash
   git clone <repository_url>
   cd temp_api
   ```

2. **Set up a virtual environment**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install fastapi uvicorn sqlalchemy psycopg passlib python-jose python-dotenv pydantic supabase
   ```

4. **Configure Environment Variables**:
   Create or verify the `.env` file in the root directory:
   ```env
   DATABASE_URL=postgresql+psycopg://user:password@host/dbname?sslmode=require
   SUPABASE_URL=https://<your-supabase-project>.supabase.co
   SUPABASE_KEY=<your-supabase-key>
   SECRET_KEY=your_secret_jwt_key
   ALGORITHM=HS256
   ACCESS_TOKEN_EXPIRE_MINUTES=60
   ```

---

## Running the Application

Run the application using Uvicorn or by executing `main.py`:

```bash
# Option 1: Direct Python execution
python main.py

# Option 2: Using Uvicorn CLI
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

Once running, access:
- **Root API Overview**: `http://localhost:8000/`
- **Health Check**: `http://localhost:8000/health`
- **Interactive Swagger Docs**: `http://localhost:8000/docs`
- **ReDoc Documentation**: `http://localhost:8000/redoc`

---

## API Reference Overview

All API v1 routes are available under `/api/v1` (and `/v1`).

### 1. Root & Health Check
| Method | Endpoint | Description | Access |
| :--- | :--- | :--- | :--- |
| `GET` | `/` | API status and documentation links | Public |
| `GET` | `/health` | Health check endpoint | Public |

### 2. Classrooms (`/api/v1/classrooms`)
| Method | Endpoint | Description | Required Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/` | Create a new classroom | `TEACHER` |
| `GET` | `/` | List all classrooms | Authenticated |
| `GET` | `/my-classrooms` | List classrooms created by current teacher | `TEACHER` |
| `GET` | `/{classroom_id}` | Get classroom details by ID | Authenticated |
| `POST` | `/{classroom_id}/join` | Join classroom as a student | `STUDENT` |

### 3. Notes (`/api/v1/notes`)
| Method | Endpoint | Description | Required Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/` | Upload a note to a classroom | `TEACHER` |
| `GET` | `/` | List all notes | Authenticated |
| `GET` | `/class/{class_id}` | Get all notes for a specific classroom | Authenticated |
| `GET` | `/{note_id}` | Get note details by ID | Authenticated |

### 4. Quizzes (`/api/v1/quizzes`)
| Method | Endpoint | Description | Required Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/` | Create a quiz question for a note | `TEACHER` |
| `GET` | `/note/{note_id}` | Get all quizzes created for a note | Authenticated |
| `GET` | `/{quiz_id}` | Get quiz details by ID | Authenticated |
| `PATCH` | `/{quiz_id}` | Update quiz question, options, or answer | `TEACHER` |
| `DELETE` | `/{quiz_id}` | Delete quiz question | `TEACHER` |

### 5. Attempts (`/api/v1/attempts`)
| Method | Endpoint | Description | Required Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/` | Start a quiz attempt from selected notes | `STUDENT` |
| `GET` | `/` | List attempts (Students see own; Teachers see all) | Authenticated |
| `GET` | `/{attempt_id}` | Get details of a specific attempt | Authenticated |

### 6. Assessments (`/api/v1/assessments`)
| Method | Endpoint | Description | Required Role |
| :--- | :--- | :--- | :--- |
| `POST` | `/` | Submit an answer to evaluate against quiz | `STUDENT` |
| `GET` | `/attempt/{attempt_id}` | View question responses & score breakdown for an attempt | Authenticated |

---

## License

This project is open-source and available under the [MIT License](LICENSE).
