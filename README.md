# Intelliscript-backend
uvicorn app.main:app --reload --port 8000
## Description

IntelliScript Backend is a FastAPI-based backend service for an educational platform. It provides APIs for user authentication, course management, assessments, student progress tracking, and AI-powered chat interactions. The platform supports multiple roles: teachers, students, and instructors, enabling comprehensive educational workflows including assessment creation, grading, file uploads, and LLM integration.

## Installation

1. Clone the repository.
2. Install dependencies: `pip install -r requirements.txt`
3. Set up environment variables (see `app/core/config.py` for details).
4. Run database migrations: `alembic upgrade head`
5. Start the server: `uvicorn app.main:app --reload`

## Project Structure

```
.
├── .gitignore
├── README.md
├── alembic.ini
├── hashPassword.py
├── requirements.txt
├── app/
│   ├── main.py
│   ├── api/
│   │   ├── v1/
│   │   │   ├── assessments.py
│   │   │   ├── auth.py
│   │   │   ├── chat.py
│   │   │   ├── courses.py
│   │   │   ├── students.py
│   │   │   └── teachers.py
│   │   └── v2/
│   ├── core/
│   │   ├── config.py
│   │   ├── deps.py
│   │   └── security.py
│   ├── db/
│   │   ├── models.py
│   │   └── session.py
│   ├── schemas/
│   │   ├── auth.py
│   │   ├── common.py
│   │   └── instructors.py
│   └── services/
│       ├── email_service.py
│       ├── llm_gateway.py
│       └── storage_service.py
└── migrations/
    ├── README
    ├── env.py
    ├── script.py.mako
    └── versions
```

## API Overview (brief)

- **Base URL**: `http://localhost:8000`
- **Docs**: Swagger UI at `/docs`, ReDoc at `/redoc`
- **Auth**: JWT Bearer token. Include header: `Authorization: Bearer <token>`

### Auth
- `POST /auth/login` — obtain access token
  - Body:
    ```json
    { "username": "user@example.com", "password": "secret" }
    ```
  - Response:
    ```json
    { "access_token": "<jwt>" }
    ```

### Chat
- `GET /chat/home` — brief dashboard for the current user
- `POST /chat/ask` — ask LLM a question
  - Form/JSON field: `question` (string)

### Teachers
- `POST /teachers/me/instructors` — create instructor under current teacher
- `POST /teachers/me/instructors/{instructor_id}/courses` — grant course access to instructor

### Courses
- `GET /courses/teacher` — list current teacher's courses
- `GET /courses/{course_id}/students` — roster for a course

### Assessments
- `POST /assessments/course/{course_id}` — create assessment
- `GET /assessments/course/{course_id}` — list assessments for course
- `POST /assessments/{assessment_id}/files` — upload assessment file (multipart)
- `GET /assessments/mine/{course_id}` — list assessments for student in a course
- `POST /assessments/{assessment_id}/submit` — submit assessment (multipart)
- `GET /assessments/{assessment_id}/result` — current student’s result
- `GET /assessments/{assessment_id}/submissions` — list submissions (teacher)
- `PATCH /assessments/submissions/{submission_id}/grade` — grade a submission

### Students
- `GET /students/me/courses` — list enrolled courses
- `GET /students/me/progress` — aggregate marks by course

## Configuration

Environment variables are read in `app/core/config.py`:

- `DATABASE_URL` — SQLAlchemy database URL
- `JWT_SECRET` — JWT signing secret (HS256)
- `FILE_STORE` — upload directory
- `SMTP_*` and `MAIL_FROM` — outbound email settings

## Running

- Local dev: `uvicorn app.main:app --reload`
- Open API docs: visit `http://localhost:8000/docs`
