from typing import Optional,List
from pydantic import BaseModel,Field
from enum import IntEnum


class Priority(IntEnum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3




class BaseTodo(BaseModel):
    title: str = Field(...,description="title of the todo")
    description: Optional[str] = Field(None,description="Description of the todo")
    is_done: bool = Field(default=False ,description="Bool value of if the task has been done.")
    priority: Priority = Field(default=Priority.LOW, description="Priority of the todo")

#class Todo(BaseTodo):
    #id: int = Field(...,description="unique identifier of the todo")

class TodoCreate(BaseTodo):
    pass

class TodoUpdate(BaseModel):
    title: Optional[str] = Field(None,description="title of the todo")
    description: Optional[str] = Field(None,description="Description of the todo")
    is_done: Optional[bool] = Field(None ,description="Bool value of if the task has been done.")
    priority: Optional[Priority] = Field(None, description="Priority of the todo")

