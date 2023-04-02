from fastapi import FastAPI, status, HTTPException
from database import Base, engine
from sqlalchemy.orm import Session
import models
import schemas


Base.metadata.create_all(engine)


app = FastAPI()


@app.get("/")
async def root():
    return "Todo API Works"


@app.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(todo: schemas.ToDo):
    session = Session(bind=engine, expire_on_commit=False)
    tododb = models.ToDo(task=todo.task)
    session.add(tododb)
    session.commit()
    id = tododb.id
    session.close()
    return f"created todo item with id {id}"


@app.get("/todo/{id}")
async def get_todo(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(models.ToDo).get(id)
    # todo = session.query(ToDo).filter(ToDo.id == id).first()
    session.close()
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found with id " + str(id))
    return todo


@app.put("/todo/{id}")
async def update_todo(id: int, task: str):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(models.ToDo).get(id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found with id " + str(id))
    todo.task = task
    session.commit()
    session.close()
    return "updated todo item with id " + str(id)


@app.delete("/todo/{id}")
async def delete_todo(id: int):
    session = Session(bind=engine, expire_on_commit=False)
    todo = session.query(models.ToDo).get(id)
    if not todo:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Todo not found with id " + str(id))
    session.delete(todo)
    session.commit()
    session.close()
    return "deleted todo item with id " + str(id)


@app.get("/todo")
async def get_todos():
    session = Session(bind=engine, expire_on_commit=False)
    todos = session.query(models.ToDo).all()
    session.close()
    return todos

