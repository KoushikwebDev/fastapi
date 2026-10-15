from pydantic import BaseModel, field_validator, model_validator, computed_field

class User(BaseModel):
    id: int
    username: str
    password: str
    confirm_password: str

    @field_validator('username')
    def validate_username(cls, value):
        if len(value) < 3:
            raise ValueError('Username must be at least 3 characters long')
        return value
    
    # it will run once all the fields are validated
    @model_validator(mode='after')
    def validate_model(cls, model):
        if model.password != model.confirm_password:
            raise ValueError('Password and confirm password must be the same')
        return model



class Product(BaseModel):
    price : float
    quantity : int

    # here this total_price field is calculating dynamically at runtime
    @computed_field
    @property
    def total_price(self):
        return self.price * self.quantity