from pydantic import BaseModel
from typing import Optional, Dict


class ErrorResponse(BaseModel):
    code: str = 'E00'
    msg: str = 'An error has occurred!'
    data: Optional[Dict] = {}
    status: bool = False


class SuccessResponse(BaseModel):
    msg: str = 'Success!'
    code: str = '01'
    data: Optional[Dict] = {}
    status: bool = True