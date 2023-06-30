from typing import Optional, List, Tuple
from ninja import Schema, Field
from datetime import datetime

class CreateTaskSchema():
    user_id: str
    section: str
    title: str
    description: str
    points: int
    start_date: datetime 
    due_date: datetime
    members: List[str]