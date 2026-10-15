from typing import List, Optional
from pydantic import BaseModel, Field


class Address(BaseModel):
    id: int
    street_name : str
    house_number: int
    city: str
    pin_code: int
    user_id: int

class User(BaseModel):
    id: int
    name: str
    email: str
    address : Address
    phone_number: List[str]
    address: Address # reference to the Address model        
    
class Comment(BaseModel):
    comment_id : int
    comment: str
    user_id: int
    replies: Optional[List["Comment"]] = None # self referential => forward referencing

Comment.model_rebuild() # this is the line to be added when we are using self referential models

# Example
comment_data = Comment(
    comment_id=1,
    comment = "This is a comment",
    user_id = 1,
    replies = [
        Comment(
            comment_id=2,
            comment = "This is a reply",
            user_id = 2,
            replies = [
                Comment(
                    comment_id=3,
                    comment = "This is a reply to a reply",
                    user_id = 3,
                    replies = []
                )
            ]
        ),
        Comment(
            comment_id=4,
            comment = "This is another reply",
            user_id = 4,
            replies = []
        )
    ]
)

class Post(BaseModel):
    post_id : int
    title: str
    content: str
    tags: List[str]
    comments: List[Comment] # reference to the Comment model
    