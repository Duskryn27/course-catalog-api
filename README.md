# Course Catalog API

A REST API for a university course catalog built with FastAPI and Pydantic.

## Features

- FastAPI REST API
- Pydantic course model
- Course filtering by elective status
- Course sorting by popularity or title
- Pagination with page and page_size
- Course lookup by ID
- Automatic Swagger documentation
- 404 handling for missing courses

## API Endpoints

### GET /

Returns a simple API status message.

### GET /courses

Returns a list of courses.

Supported query parameters:

- is_elective — filter courses by elective status
- sort — sort by popular or title
- page — page number
- page_size — number of courses per page

Examples:

/courses
/courses?is_elective=true
/courses?sort=title
/courses?page=1&page_size=2

### GET /courses/{course_id}

Returns a single course by its ID.

Example:

/courses/ai-integration

If the course does not exist, the API returns HTTP 404.

## Project Structure

course-catalog-api/
├── .gitignore
├── data.py
├── main.py
├── models.py
├── README.md
└── requirements.txt

## Technologies

- Python
- FastAPI
- Pydantic
- Uvicorn

## Installation

Create and activate a virtual environment:

py -m venv .venv
.\.venv\Scripts\Activate.ps1

Install dependencies:

pip install -r requirements.txt

## Running the API

Start the development server:

fastapi dev main.py

The API will be available at:

http://127.0.0.1:8000

Interactive Swagger documentation:

http://127.0.0.1:8000/docs