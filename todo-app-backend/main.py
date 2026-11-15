from contextlib import asynccontextmanager
from typing import Annotated

from fastapi import Depends, FastAPI, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import select
from sqlalchemy.orm import Session

from database import Base, engine, get_db
from models import Task, Category
from schemas import (
    TaskCreateSchema,
    TaskUpdateSchema,
    TaskReadSchema,
    CategoryCreateSchema,
    CategoryUpdateSchema,
    CategoryReadSchema
)

@asynccontextmanager
async def lifespan(app: FastAPI):
    Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://127.0.0.1:3000",
    ],
    allow_methods=["*"],
    allow_headers=["*"],
)

SessionDep = Annotated[Session, Depends(get_db)]

@app.get("/tasks", response_model=list[TaskReadSchema])
def read_tasks(db: SessionDep):
    return db.scalars(select(Task)).all()


@app.post("/tasks", response_model=TaskReadSchema, status_code=status.HTTP_201_CREATED)
def create_task(payload: TaskCreateSchema, db: SessionDep):
    new_task = Task(title=payload.title)

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task


@app.patch("/tasks/{task_id}", response_model=TaskReadSchema)
def update_task(task_id: str, payload: TaskUpdateSchema, db: SessionDep,):
    task = db.get(Task, task_id)

    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )

    if payload.title is not None:
        task.title = payload.title

    if payload.completed is not None:
        task.completed = payload.completed

    db.commit()
    db.refresh(task)

    return task


@app.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str, db: SessionDep):
    task = db.get(Task, task_id)
    if task is None:
        raise HTTPException(
            status_code=404,
            detail="Task not found",
        )
    db.delete(task)
    db.commit()



@app.get("/categories", response_model=list[CategoryReadSchema])
def read_categories(db: SessionDep):
    return db.scalars(select(Category)).all()


@app.post("/categories", response_model=CategoryReadSchema, status_code=status.HTTP_201_CREATED)
def create_categories(payload: CategoryCreateSchema, db: SessionDep):
    new_category = Category(name=payload.name,)

    db.add(new_category)
    db.commit()
    db.refresh(new_category)

    return new_category


@app.patch("/categories/{category_id}", response_model=CategoryReadSchema)
def update_category(category_id: str, payload: CategoryUpdateSchema, db: SessionDep,):
    category = db.get(Category, category_id)

    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    if payload.name is not None:
        category.name = payload.name

    db.commit()
    db.refresh(category)

    return category


@app.delete("/categories/{category_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(category_id: str, db: SessionDep,):
    category = db.get(Category, category_id)
    if category is None:
        raise HTTPException(
            status_code=404,
            detail="Category not found",
        )

    db.delete(category)
    db.commit()