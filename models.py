from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class CamelModel(BaseModel):
    model_config = ConfigDict(
        alias_generator=to_camel,
        validate_by_name=True,
    )


class Course(CamelModel):
    id: str
    title: str
    description: str
    credits: int
    is_elective: bool = False
    likes: int = 0

class EnrollmentCreate(CamelModel):
    course_id: str
    student_name: str

class Enrollment(EnrollmentCreate):
    id: int