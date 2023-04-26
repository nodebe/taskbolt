from typing import Optional, List, Tuple
from ninja import Schema, Field

class CreateSectionSchema(Schema):
    user_id: str
    project_id: str
    title: str

class SectionResponseSchema(Schema):
    id: str
    project_id: str
    title: str