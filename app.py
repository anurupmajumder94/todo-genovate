from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List

app = FastAPI(title="Simple Todo App")

# ---------------- Models ----------------
class Todo(BaseModel):
    id: int
    title: str
    completed: bool = False


class TodoCreate(BaseModel):
    title: str


# ---------------- In-memory DB ----------------
todos: List[Todo] = []


# ---------------- Routes ----------------
@app.get("/todos", response_model=List[Todo])
def get_todos():
    return todos


@app.post("/todos", response_model=Todo)
def create_todo(todo: TodoCreate):
    new_todo = Todo(
        id=len(todos) + 1,
        title=todo.title,
        completed=False
    )
    todos.append(new_todo)
    return new_todo


@app.put("/todos/{todo_id}", response_model=Todo)
def update_todo(todo_id: int, completed: bool):
    for todo in todos:
        if todo.id == todo_id:
            todo.completed = completed
            return todo
    raise HTTPException(status_code=404, detail="Todo not found...")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
    for i, todo in enumerate(todos):
        if todo.id == todo_id:
            todos.pop(i)
            return {"message": "Todo deleted"}
    raise HTTPException(status_code=404, detail="Todo not found...")
