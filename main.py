from typing import List
from fastapi import FastAPI, status, HTTPException, Depends
from database import Base, engine, SessionLocal
from sqlalchemy.orm import Session
import models
import schemas


Base.metadata.create_all(engine)


app = FastAPI()


# Helper function to get database session
def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()


@app.get("/")
async def root():
    return "Todo API Works"


@app.post("/todo", response_model=schemas.ToDo, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.ToDo, session: Session = Depends(get_session)):
    tododb = models.ToDo(task=todo.task)
    session.add(tododb)
    session.commit()
    session.refresh(tododb)
    return tododb


@app.get("/todo/{id}", response_model=schemas.ToDo)
async def get_todo(id: int, session: Session = Depends(get_session)):
    todo = session.query(models.ToDo).get(id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found with id " + str(id))
    return todo


@app.put("/todo/{id}", response_model=schemas.ToDo)
async def update_todo(id: int, task: str, session: Session = Depends(get_session)):
    todo = session.query(models.ToDo).get(id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found with id " + str(id))
    todo.task = task
    session.commit()
    session.refresh(todo)
    return todo


@app.delete("/todo/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(id: int, session: Session = Depends(get_session)):
    todo = session.query(models.ToDo).get(id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found with id " + str(id))
    session.delete(todo)
    session.commit()
    return "Todo deleted"


@app.get("/todo", response_model=list[schemas.ToDo])
async def get_todos():
    session = Session(bind=engine, expire_on_commit=False)
    todos = session.query(models.ToDo).all()
    session.close()
    return todos

