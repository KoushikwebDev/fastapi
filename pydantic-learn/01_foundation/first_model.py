from pydantic import BaseModel

class User(BaseModel):
    id: int
    name: str
    email: str
    is_active: bool = True # default value


input_data = {"id" : 1, "name" : "Koushik", "email": "kl@gmail.com", "is_active" : True}
input_data2 = {"id" : "101", "name" : "Koushik", "email": "kl@gmail.com", "is_active" : "True"}

try:
    user = User(**input_data)
    print(user)
except Exception as e:
    print(e)

try:
    user2 = User(**input_data2)
    print(user2)
except Exception as e:
    print(e)    
    