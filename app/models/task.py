from pydantic import BaseModel, Field
from typing import Optional

class TaskCreate(BaseModel):
    id: int
    title: str = Field(..., min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    status: str = Field("do wykonania", pattern="^(do wykonania|w trakcie|zakończone)$")

class TaskUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=3, max_length=100)
    description: Optional[str] = Field(None, max_length=300)
    status: Optional[str] = Field(None, pattern="^(do wykonania|w trakcie|zakończone)$")