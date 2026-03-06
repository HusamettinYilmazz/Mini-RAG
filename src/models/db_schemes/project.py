from pydantic import BaseModel, Field, field_validator
from typing import Optional
from bson.objectid import ObjectId

class Project(BaseModel):
    _id: Optional[ObjectId]
    project_id: str= Field(..., min_length=1)

    @field_validator('project_id')
    def validate_project_id(cls, val):
        if not val.isalnum():
            raise ValueError("project_id must be alphnumeric")
        return val
    
    class Config:
        arbitrary_types_allowed = True