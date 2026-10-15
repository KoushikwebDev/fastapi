from pydantic import BaseModel, ConfigDict
from typing import List,Dict,Any
from datetime import datetime

class Address(BaseModel):
    id : int
    street_name : str
    house_number : int
    city : str
    pin_code : int
    user_id : int

class User(BaseModel):
    id : int
    name : str
    email : str
    phone_number : List[str]
    address : Address
    is_active : bool
    created_at : datetime

    model_config = ConfigDict(
        json_encoders = {
            datetime: lambda v: v.strftime("%Y-%m-%d %H:%M:%S")
        }
    )


user_data = {
    "id" : 1,
    "name" : "Koushik",
    "email" : "[EMAIL_ADDRESS]",
    "phone_number" : ["1234567890", "9876543210"],
    "address" : {
        "id" : 1,
        "street_name" : "123 Main St",
        "house_number" : 123,
        "city" : "New York",
        "pin_code" : 10001,
        "user_id" : 1
    },
    "is_active" : True,
    "created_at" : datetime(2022, 1, 1)
}

# converting dict to model instance
user = User(**user_data)

# print(user)

# converting model instance to dict
user_dict = user.model_dump()
print(user_dict)


print("\n\n\n")

# converting model instance to json
user_json = user.model_dump_json()
print(user_json)

