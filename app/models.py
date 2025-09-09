from typing import List, Optional
from sqlmodel import Field, SQLModel,Relationship

from schemas.TodoSchema import Priority


class Todo(SQLModel,table=True):
    id: int | None = Field(default=None,primary_key=True)
    title:str = Field(index=True)
    description: Optional[str] = Field(nullable=True,default=None)
    priority: Priority 
    user_id: Optional[int] = Field(default=None, foreign_key="user.id")
    user: Optional["User"] = Relationship(back_populates="todos")

class User(SQLModel,table = True):
    id: Optional[int] = Field(default=None,primary_key=True)
    email:str = Field(unique=True,index=True)
    hashed_password: str = Field()
    todos: List["Todo"] = Relationship(back_populates="user")
    is_admin: bool = Field(default=False)


