from sqlmodel import SQLModel

class UserCreate(SQLModel):
    email:str
    password:str

class UserPublic(SQLModel):
    id:int
    email:str
    is_admin: bool
    

