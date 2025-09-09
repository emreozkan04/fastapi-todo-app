from fastapi import Depends, FastAPI, Form,HTTPException,Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from sqlmodel import Session, select
from app.security import get_admin_user, get_current_user, hash_password,verify_password,create_access_token
from schemas.TodoSchema import TodoCreate,TodoUpdate,Priority
from fastapi.templating import Jinja2Templates
from typing import List
from contextlib import asynccontextmanager
from app.database import create_db_and_tables, get_session
from app.models import Todo, User
from schemas.UserSchema import UserCreate, UserPublic

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("Creating database and tables...")
    create_db_and_tables()
    yield

app = FastAPI(lifespan=lifespan)

app.mount("/static", StaticFiles(directory="app/static"), name="static")
templates = Jinja2Templates(directory="app/templates")

@app.get("/",response_class=HTMLResponse)
def home(request:Request):
     return templates.TemplateResponse("index.html", {"request": request})
@app.get("/login", response_class=HTMLResponse)
def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/login")
def login(
    session:Session = Depends(get_session),
    username: str = Form(...),
    password: str = Form(...)):

    user = session.exec(select(User).where(User.email == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        raise HTTPException(401, detail="Incorrect email or password!")
    access_token = create_access_token(data={"sub":user.email})
    return {"access_token" :access_token, "token_type":"bearer"}


@app.get("/todos",response_model=List[Todo])
def get_todos(session: Session = Depends(get_session),
              current_user: User = Depends(get_current_user)):
    todos = session.exec(select(Todo).where(Todo.user_id == current_user.id)).all()
    return todos

@app.get("/todos/{id}",response_model=Todo)
def get_todo(id:int,session:Session = Depends(get_session),
             current_user: User = Depends(get_current_user)):
    todo = session.exec(select(Todo).where(Todo.user_id == current_user.id).where(Todo.id == id)).first()
    if not todo:
        raise HTTPException(404,detail="Item not found!")
    return todo


@app.post("/create_todo",response_model=Todo)
def create_todo(todo:TodoCreate,session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)):
    todo_to_db = Todo.model_validate(todo)
    todo_to_db.user_id = current_user.id
    session.add(todo_to_db)
    session.commit()
    session.refresh(todo_to_db)
    return todo_to_db

@app.delete("/todo/{id}",response_model=Todo)
def delete_todo(id:int,session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)):
    todo_to_delete = session.get(Todo,id)
    if not todo_to_delete or todo_to_delete.user_id != current_user.id:
        raise HTTPException(404,detail="Todo not Found!")
    session.delete(todo_to_delete)
    session.commit()
    return todo_to_delete

@app.put("/todo/{id}", response_model=Todo)
def update_todo(modified_todo: TodoUpdate, id: int,session: Session = Depends(get_session),
                current_user: User = Depends(get_current_user)):
    db_todo = session.get(Todo,id)
    if not db_todo or db_todo.user_id != current_user.id:
        raise HTTPException(404, detail="Item not Found!")
    
    todo_data = modified_todo.model_dump(exclude_unset=True)
    for key,value in todo_data.items():
        setattr(db_todo,key,value)
        
    session.add(db_todo)
    session.commit()
    session.refresh(db_todo)
    return db_todo


@app.get("/users",response_model=List[UserPublic])
def get_users(session: Session = Depends(get_session),
              admin_user: User = Depends(get_admin_user)):
    
    users = session.exec(select(User)).all()
    return users

@app.get("/users/{id}",response_model=UserPublic)
def get_user(id:int,session:Session = Depends(get_session),
             admin_user:User = Depends(get_admin_user)):
    
    user = session.get(User,id)
    if not user:
        raise HTTPException(404,detail="User Not Found!")
    return user

@app.post("/register",response_model=UserPublic)
def create_user(user:UserCreate,session:Session = Depends(get_session)):
    db_user = session.exec(select(User).where(User.email == user.email)).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")

    hashed_pass = hash_password(user.password)
    new_user = User(email=user.email,hashed_password=hashed_pass)
    session.add(new_user)
    session.commit()
    session.refresh(new_user)

    return new_user

@app.delete("/delete_user/{id}",response_model=UserPublic)
def delete_user(id:int, session:Session = Depends(get_session),
                admin_user : User = Depends(get_admin_user)):
    user_to_delete = session.get(User,id)
    if not user_to_delete:
        raise HTTPException(404,detail="User Not Found!")
    session.delete(user_to_delete)
    session.commit()
    return user_to_delete








