# Course Catalog API

A REST API for a university course catalog built with FastAPI and Pydantic. This backend provides course data, filtering, sorting, pagination, course likes, and student enrollments for the Course Catalog frontend.

## Features

- FastAPI REST API
- Pydantic models with camelCase JSON aliases
- Course filtering by elective status
- Course sorting by popularity or title
- Pagination with `page` and `page_size`
- Course lookup by ID
- Course likes with `POST` requests
- Student enrollment creation and listing
- Request validation with HTTP 422 responses
- HTTP 404 handling for missing courses
- CORS configured for the frontend origin
- Automatic OpenAPI and Swagger documentation

## API Endpoints

### `GET /`

Returns a message confirming that the API is running.

### `GET /courses`

Returns a list of courses.

Supported query parameters:

- `is_elective` — filter by elective status (`true` or `false`)
- `sort` — sort by popularity or title
- `page` — page number
- `page_size` — number of courses per page

Examples:

```text
/courses
/courses?is_elective=true
/courses?sort=title
/courses?page=1&page_size=2
```

The query parameter uses snake_case: `is_elective`.

### `GET /courses/{course_id}`

Returns a single course by its ID.

Example:

```text
/courses/ai-integration
```

Returns HTTP 404 if the course does not exist.

### `POST /courses/{course_id}/like`

Increments the like count for a course and returns the updated course.

Example:

```text
POST /courses/ai-integration/like
```

Returns HTTP 404 if the course does not exist.

### `POST /enrollments`

Creates a student enrollment.

Example JSON request body:

```json
{
  "courseId": "web-security",
  "studentName": "Aigerim"
}
```

A successful request returns HTTP 201 and the created enrollment. The student name must contain at least two characters. Invalid input returns HTTP 422, and an unknown course ID returns HTTP 404.

### `GET /enrollments`

Returns the list of enrollments created during the current backend process.

## JSON Naming Convention

The API uses Pydantic models with a camelCase alias generator.

Examples of JSON fields:

- `isElective`
- `courseId`
- `studentName`

The course-filter query parameter remains `is_elective`, because query parameters are defined separately from JSON field aliases.

## CORS Configuration

The backend allows requests from this exact frontend origin:

```text
http://localhost:3000
```

The origin includes the scheme, host, and port, without a trailing slash.

Requests from other origins are not granted CORS permission. The configuration supports the methods and headers required by the frontend, including JSON enrollment requests and their browser preflight requests.

## Project Structure

```text
course-catalog-api/
├── .gitignore
├── data.py
├── main.py
├── models.py
├── README.md
└── requirements.txt
```

## Technologies

- Python
- FastAPI
- Pydantic
- Uvicorn

## Installation

Create and activate a virtual environment in PowerShell:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

## Running the API

Start the development server:

```powershell
fastapi dev main.py
```

The API will be available at:

- API root: `http://localhost:8000/`
- Interactive Swagger documentation: `http://localhost:8000/docs`
- OpenAPI schema: `http://localhost:8000/openapi.json`

## Validation and Testing

The following behaviors should be verified using Swagger, the frontend, or HTTP requests:

- Course endpoints return course data.
- Course filtering and sorting work.
- A valid like request increments the course's like count.
- A valid enrollment returns HTTP 201.
- An enrollment with a student name shorter than two characters returns HTTP 422.
- Requests for unknown course IDs return HTTP 404.
- The configured frontend origin receives the appropriate CORS permission.
- A JSON enrollment request from the browser can complete its CORS preflight.
- Responses use camelCase JSON field names.

## Data Persistence

Course data and likes are stored in backend memory. Enrollments are also stored in memory. These values may reset when the backend process restarts. This implementation does not use a persistent database.

## Related Project

The frontend is the Course Catalog Next.js application. Run the frontend and backend together to test the complete integration.