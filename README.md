# Course Catalog API

Backend REST API for a university course catalog built with FastAPI, Pydantic, SQLAlchemy 2.1, PostgreSQL, and Alembic migrations.

This project provides persistent course data, student management, enrollments, course statistics, filtering, sorting, pagination, and database error handling.

## Features

- FastAPI REST API
- SQLAlchemy models and PostgreSQL persistence
- Pydantic schemas with camelCase JSON aliases
- Course filtering by elective status and difficulty level
- Course sorting by popularity or title
- Pagination with `page` and `page_size`
- Course lookup by ID
- Atomic course likes using SQL UPDATE
- Student creation and enrollment management
- Enrollment listing with JOIN queries
- Course statistics using LEFT JOIN and COUNT
- Database constraint error handling (409, 404)
- Alembic database migrations
- CORS configured for the frontend origin
- Automatic OpenAPI and Swagger documentation

## API Endpoints

### `GET /`

Returns a message confirming that the API is running.

### `GET /courses`

Returns a list of courses.

Supported query parameters:

- `is_elective` — filter by elective status (`true` or `false`)
- `level` — filter by difficulty (`beginner`, `intermediate`, `advanced`)
- `sort` — sort by popularity or title
- `page` — page number
- `page_size` — number of courses per page

Examples:

```text
/courses
/courses?is_elective=true
/courses?level=beginner
/courses?level=beginner&is_elective=true
/courses?sort=title
/courses?page=1&page_size=2
```

The query parameter `is_elective` uses snake_case. The API response uses camelCase: `isElective`.

### `GET /courses/{course_id}`

Returns a single course by its ID.

Example:

```text
/courses/ai-integration
```

Returns HTTP 404 if the course does not exist.

Course responses include the `level` field.

### `POST /courses/{course_id}/like`

Atomically increments the like count for a course using a database-side UPDATE and returns the updated course.

Example:

```text
POST /courses/ai-integration/like
```

Returns HTTP 404 if the course does not exist.

### `POST /students`

Creates a new student.

Example JSON request:

```json
{
  "name": "Aigerim Sadykova",
  "email": "aigerim@example.com"
}
```

Returns HTTP 201 and the created student with a database-generated ID.

The name must contain at least two characters, and the email must be valid.

### `POST /enrollments`

Creates an enrollment for an existing student in an existing course.

Example JSON request:

```json
{
  "courseId": "web-security",
  "studentId": 1
}
```

Returns HTTP 201 and the created enrollment.

The API now expects `studentId` instead of `studentName`. A student must be created first using `POST /students`.

### `GET /enrollments`

Returns all enrollments with additional information obtained through JOIN queries:

- Enrollment ID
- Course ID
- Student ID
- Enrollment timestamp
- Course title
- Student name

### `GET /stats/courses`

Returns the number of enrollments for each course.

Uses LEFT JOIN and `COUNT(enrollments.id)` so courses without enrollments are also included with a count of zero.

## JSON Naming Convention

The API uses Pydantic models with a camelCase alias generator.

Examples of JSON fields:

- `isElective`
- `courseId`
- `studentId`
- `studentName`
- `enrolledAt`
- `courseTitle`

The query parameters remain snake_case where defined separately, for example `is_elective`.

## Database Error Handling

Database constraint violations are translated into appropriate HTTP responses.

| Constraint | HTTP status | Description |
|------------|-------------|-------------|
| `students_email_key` | 409 | Student email already exists |
| `enrollments_course_id_student_id_key` | 409 | Student is already enrolled in this course |
| `enrollments_course_id_fkey` | 404 | Course not found |
| `enrollments_student_id_fkey` | 404 | Student not found |
| `students_name_check` | 422 | Invalid student name; normally caught by Pydantic first |

Unknown database constraint violations are re-raised as server errors.

## CORS Configuration

The backend allows requests from this frontend origin:

```text
http://localhost:3000
```

The origin includes the scheme, host, and port, without a trailing slash.

The configuration supports the methods and headers required by the frontend, including JSON requests and browser preflight requests.

## Data Persistence

Course, student, and enrollment data are stored in PostgreSQL.

Unlike the earlier in-memory implementation, data and course likes remain stored after the FastAPI server restarts.

SQLAlchemy manages database operations through sessions. Alembic manages database schema changes through versioned migrations.

## Technologies

- Python
- FastAPI
- Pydantic
- SQLAlchemy 2.1
- PostgreSQL
- Psycopg 3
- Alembic
- Uvicorn

## Project Structure

```text
course-catalog-api/
├── alembic/
│   ├── versions/
│   │   ├── 0001_create_catalog_tables.py
│   │   └── 0002_add_course_level.py
│   ├── env.py
│   └── script.py.mako
├── .env.example
├── .gitignore
├── alembic.ini
├── check_db.py
├── check_models.py
├── config.py
├── db.py
├── main.py
├── models.py
├── schemas.py
├── requirements.txt
├── seed.sql
└── try_errors.py
```

The `.env` file contains local database credentials and must not be committed to Git.

## Installation and Running

### Requirements

- Python 3.11 or newer
- PostgreSQL 16 or newer
- Git

The following commands use PowerShell and the local PostgreSQL port `5433`.

### 1. Create the database role and database

As the PostgreSQL superuser, execute:

```sql
CREATE ROLE catalog_app LOGIN PASSWORD 'change-me';
CREATE DATABASE course_catalog OWNER catalog_app;
```

Skip this step if the role and database already exist.

The password shown is an example for a local training environment. Use your own password.

### 2. Create a virtual environment

```powershell
py -m venv .venv
```

### 3. Install dependencies

```powershell
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

### 4. Configure environment variables

Copy the example file:

```powershell
Copy-Item .env.example .env
```

Edit `.env`:

```env
DATABASE_URL=postgresql+psycopg://catalog_app:YOUR_PASSWORD@127.0.0.1:5433/course_catalog
SQL_ECHO=true
```

Replace `YOUR_PASSWORD` with the password configured for `catalog_app`.

Do not commit `.env` or share database credentials.

### 5. Apply database migrations

```powershell
.\.venv\Scripts\alembic.exe upgrade head
```

Alembic applies both migrations and creates the database structure.

### 6. Insert initial data

```powershell
& "C:\Program Files\PostgreSQL\18\bin\psql.exe" -h localhost -p 5433 -U catalog_app -d course_catalog -v ON_ERROR_STOP=1 -f seed.sql
```

The seed script inserts:

- 6 courses
- 3 students
- 6 enrollments

**Warning:** `seed.sql` uses `TRUNCATE ... RESTART IDENTITY`. It deletes existing training data and resets ID counters. Use it only with the training database.

### 7. Verify the database

```powershell
.\.venv\Scripts\python.exe check_db.py

.\.venv\Scripts\python.exe check_models.py

.\.venv\Scripts\alembic.exe check
```

### 8. Start the API

```powershell
.\.venv\Scripts\fastapi.exe dev main.py
```

The API will be available at:

- API root: http://localhost:8000/
- Swagger documentation: http://localhost:8000/docs
- OpenAPI schema: http://localhost:8000/openapi.json

## Migrations

| Command | Description |
|---------|-------------|
| `alembic upgrade head` | Applies all missing migrations |
| `alembic downgrade -1` | Rolls back the latest migration |
| `alembic current` | Shows the current database revision |
| `alembic history` | Displays the migration history |
| `alembic heads` | Shows current migration heads |
| `alembic revision --autogenerate -m "text"` | Generates a migration draft |
| `alembic check` | Checks for differences between models and database |
| `alembic upgrade 0001:0002 --sql` | Prints migration SQL without executing it |
| `alembic stamp head` | Marks the database as up to date without executing migrations |

### Migration history

| Revision | Description |
|----------|-------------|
| `0001` | Creates courses, students, and enrollments tables, constraints, and indexes |
| `0002` | Adds the required course difficulty level using a three-step migration |

Migration `0002` performs three operations:

1. Adds `courses.level` as a nullable TEXT column.
2. Populates existing rows: elective courses receive `beginner`, other courses receive `intermediate`.
3. Changes `level` to NOT NULL.

The downgrade operation removes the `level` column.

## Experiment Log

| # | Experiment | What I saw | Cause | How I fixed it |
|---|------------|------------|-------|----------------|
| 1 | Changed the `uq` naming convention template | Model names differed from PostgreSQL names: `students_email_unique` and `enrollments_course_id_unique`. | The template used only the first column name instead of all columns. | Restored `%(table_name)s_%(column_0_N_name)s_key`. |
| 2 | Removed `min_length` from `StudentIn` and sent name `N` | HTTP 500; PostgreSQL reported `students_name_check`. | Pydantic allowed the short name, so the database CHECK constraint rejected the INSERT. | Restored `Field(min_length=2)`. |
| 3 | Changed `students_email_key` to `students_email_uniq` in the error dictionary | Duplicate email returned HTTP 500; PostgreSQL reported `students_email_key`. | The dictionary key did not match the actual constraint name. | Restored the exact constraint name. |
| 4 | Removed `NOT NULL` from `courses.title` and changed its type to `VARCHAR(100)` | `alembic check` detected `modify_nullable` and `modify_type`. | Database schema differed from the SQLAlchemy model. | Restored NOT NULL and the TEXT type. |
| 5 | Applied autogenerated migration `0002` to a populated table | `NotNullViolation`: column `level` contains NULL values. The database remained at revision `0001`. | Existing rows had no value for the newly added required column. | Rewrote migration into three steps: add nullable column, fill rows, set NOT NULL. |
| 6 | Commented out `import models` in `alembic/env.py` | Alembic detected removed tables `courses`, `students`, `enrollments` and the student index. | `Base.metadata` was empty because models were not imported. | Restored the import and deleted the experimental migration. |
| 7 | Added `phone: Mapped[str \| None]` to Student without a migration | `alembic check` detected the added column `students.phone`. | The model contained a column absent from the database. | Removed the temporary field and confirmed a clean check. |
| 8 | Created two migrations from revision `0002` | `alembic heads` showed `0003` and `0004`; `upgrade head` failed with `Multiple head revisions`. | Two independent branches had no single common head. | Created a merge revision, verified one head, then removed all experimental migrations and restored `0002` as the only head. |

## Decisions

### 1. Why use constraint names instead of SQLSTATE, and why catch errors after commit?

SQLSTATE identifies a general error category. For example, `23505` identifies a uniqueness violation, but our database has multiple UNIQUE constraints with different meanings.

The exact constraint name identifies the violated rule and allows the API to return the correct response, such as an existing email or duplicate enrollment.

Catching the error after `commit()` is safer than checking with SELECT before inserting. Between a preliminary SELECT and INSERT, another request could insert the same value. This race condition makes preliminary checks unreliable. The database constraint is the final authority.

### 2. Why increment likes using a database-side UPDATE?

The application uses:

```sql
UPDATE courses
SET likes = likes + 1
WHERE id = ...;
```

The database performs the increment atomically. If the application reads the likes value, increments it in Python, and writes it back, two concurrent requests could read the same value and overwrite each other's changes. A database-side update avoids this lost-update problem.

### 3. Why is migration 0002 split into three steps?

The courses table already contains records. Adding a NOT NULL column immediately would fail because existing rows would have no value for the new column.

The migration therefore:

1. Adds the column while allowing NULL.
2. Fills existing rows according to the selected rule.
3. Changes the column to NOT NULL.

This preserves existing rows and guarantees that every course has a level after the migration.

## Migration 0002 Self-check

| What to check | Result |
|---------------|--------|
| Goal and steps | **Yes** — Adds one required TEXT column in three explicit steps. |
| Data | **Yes** — All six existing courses receive a level: electives become `beginner`, other courses become `intermediate`. |
| Renames and drops | **Yes** — Upgrade does not rename or drop existing columns. It only adds `level`. |
| Rollback | **Yes** — Downgrade removes `level`. The downgrade → upgrade cycle was tested. The downgrade intentionally removes level values; the next upgrade repopulates them using the migration rule. |
| Verification | **Yes** — Reviewed generated SQL, tested the migration in both directions, and confirmed `alembic check` reports no differences. |
| History | **Yes** — The migration chain has a single head, `0002`. The model, schema, and migration changes were committed together. |
| Application | **Yes** — Added `level` to the SQLAlchemy model and Pydantic response schema, added the API filter, and updated `seed.sql`. |

## Validation and Testing

The following behaviors were verified:

- Course endpoints return data from PostgreSQL.
- Course filtering by elective status and difficulty level works.
- Sorting and pagination work.
- Course lookup returns HTTP 404 for unknown IDs.
- Course likes use UPDATE RETURNING and persist after restart.
- Student creation returns HTTP 201.
- Enrollment creation and listing work with JOIN queries.
- Course statistics include courses with zero enrollments.
- Database constraint errors return the expected HTTP statuses.
- `try_errors.py` prints `5 of 5 as expected`.
- `alembic current` reports `0002 (head)`.
- `alembic check` reports `No new upgrade operations detected`.
- The downgrade → upgrade migration cycle works.

## Related Project

The frontend is the Course Catalog Next.js application. The backend exposes the API documented above and supports integration with the frontend running at `http://localhost:3000`.
