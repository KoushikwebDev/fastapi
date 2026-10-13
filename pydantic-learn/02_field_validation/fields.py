from pydantic import BaseModel, Field
from typing import Optional, List, Dict


class Cart(BaseModel):
    user_id: int
    items : List[str]
    quantity: Dict[str, int]


class BlogPost(BaseModel):
    title: str
    content: str
    tags: List[str]
    image_url: Optional[str] = None
    rating: Optional[int] = None

class Employee(BaseModel):
    id: int
    name: str = Field(
        ..., # it means it is required and must contain 
        min_length=3, 
        max_length=20, 
        description="Employee Name", 
        examples="Koushik Saha"
        )
    department: Optional[str] = "General"
    salary: float = Field(..., gt=20000, lt=100000, description="Salary", examples=50000)
    

