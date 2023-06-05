from typing import List
from ninja import Schema, Field
from pydantic import EmailStr
from datetime import datetime
from enum import IntEnum


class CreateProjectSchema(Schema):
    user_id: str
    name: str = Field(strip_whitespace=True, min_length=3, max_length=50)
    description: str = Field(strip_whitespace=True)
    members: List[EmailStr]


# class ProjectStatusEnum(IntEnum):
#     active = 1
#     archived = 2

class ProjectStatus(Schema):
    id: int
    status: str

class ProjectResponseSchema(Schema):
    id: str
    name: str
    description: str
    created_at: datetime
    status: ProjectStatus

class ProjectsResponseSchema(Schema):
    projects: List[ProjectResponseSchema]

class GetProjectsSchema(Schema):
    user_id: str