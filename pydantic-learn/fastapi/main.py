from fastapi import FastAPI, Depends
from pydantic import BaseModel, EmailStr

app = FastAPI()


class UserSignUp(BaseModel):
    username: str
    email: EmailStr
    password: str
    confirm_password: str

class Settings(BaseModel):
    app_name : str = "My FastAPI App"
    app_version: str = "1.0.0"
    admin_email : str = "kl@yopmail.com"

def get_settings():
    return Settings()

# app = FastAPI(title=Settings().app_name, version=Settings().app_version)

# route for root
@app.get("/")
async def root():
    return {"message" : "Welcome to My FastAPI App"}


@app.post("/register")
async def register_user(user: UserSignUp):
    # if user.password != user.confirm_password:
    #     return {"message" : "Password and confirm password do not match"}
    return {"message" : "User registered successfully", "user" : user}

@app.get("/settings")
async def get_settings_data(settings : Settings = Depends(get_settings)):
    return settings

